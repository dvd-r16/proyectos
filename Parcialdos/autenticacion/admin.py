from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from axes.admin import AccessLogAdmin as DefaultAccessLogAdmin
from axes.models import AccessLog
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

# La función exportar_pdf está bien definida aquí

def exportar_pdf(modeladmin, request, queryset):
    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="access_logs.pdf"'

    # Crear un objeto canvas para generar el PDF y definir el tamaño de la página
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4  # Tamaño de página A4 (Ancho y Alto)

    # Establecer el título del documento
    p.setFont("Helvetica-Bold", 12)  # Reducir un poco el tamaño de la fuente
    p.drawString(50, height - 40, "Reporte de Accesos")

    # Posiciones iniciales para la tabla
    y_position = height - 80  # Ajuste la posición vertical inicial
    x_offsets = [50, 140, 230, 320, 410, 500]  # Ajustar posiciones de columnas
    column_widths = [90, 90, 90, 90, 90, 90]  # Ancho de cada columna
    max_width = width - 60  # Espacio máximo permitido horizontalmente

    # Agregar encabezados de la tabla
    headers = ['Attempt Time', 'Logout Time', 'IP Address', 'Username', 'User Agent', 'Path Info']
    p.setFont("Helvetica-Bold", 10)  # Fuente y tamaño más pequeños para encabezados
    for index, header in enumerate(headers):
        p.drawString(x_offsets[index], y_position, header)

    # Reducir la posición Y para las filas
    y_position -= 20

    # Ajustar el tamaño de la fuente para el contenido
    p.setFont("Helvetica", 8)  # Reducir más el tamaño para el contenido

    # Iterar sobre los registros seleccionados y agregarlos al PDF
    for log in queryset:
        fields = [
            str(log.attempt_time),
            str(log.logout_time) if log.logout_time else '-',
            log.ip_address,
            log.username,
            log.user_agent,
            log.path_info
        ]

        # Asegurarse de no superponer textos
        for index, field in enumerate(fields):
            # Ajustar texto al ancho de columna si es necesario
            max_text_width = column_widths[index]
            text_width = stringWidth(field, "Helvetica", 8)
            if text_width > max_text_width:
                # Dividir en múltiples líneas si el texto es demasiado ancho
                max_chars = int(max_text_width / 5)  # Estimación de caracteres por línea
                lines = [field[i:i+max_chars] for i in range(0, len(field), max_chars)]
                for line in lines:
                    if y_position < 40:  # Añadir nueva página si se llega al final
                        p.showPage()
                        y_position = height - 40
                        p.setFont("Helvetica", 8)  # Ajustar fuente en nueva página
                    p.drawString(x_offsets[index], y_position, line)
                    y_position -= 10  # Espacio entre líneas divididas
            else:
                p.drawString(x_offsets[index], y_position, field)

        # Reducir la posición Y para la siguiente fila
        y_position -= 20
        if y_position < 40:  # Añadir nueva página si se llega al final
            p.showPage()
            y_position = height - 40
            p.setFont("Helvetica", 8)

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response

# Asegúrate de que estás extendiendo la clase AccessLogAdmin correctamente
DefaultAccessLogAdmin.actions = tuple(DefaultAccessLogAdmin.actions) + (exportar_pdf,)
