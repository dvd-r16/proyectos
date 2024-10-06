from django.shortcuts import render, get_object_or_404, redirect
from inventario.models import articulos
from pedidos.models import LineaPedido
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import openpyxl
from django.http import HttpResponse
# Create your views here.

def catalogo(request):
    arts = articulos.objects.all()
    return render(request, "inventario/catalogo.html", {"arts":arts})

def single_product(request, id):
    # arts = articulos.objects.all()
    product = articulos.objects.get(pk=id)
    # product_name = product.cantidad
    # print(product_name)
    return render(request, "inventario/single-product.html", {"product":product})

@login_required
def curso_page(request, id):
    # Obtener el curso específico
    curso = get_object_or_404(articulos, pk=id)

    # Verificar si el usuario es el catedrático del curso
    es_catedratico = request.user == curso.catedratico.user

     # Mensaje de depuración
    if es_catedratico:
        print(f"El usuario {request.user} es el catedrático del curso.")
    else:
        print(f"El usuario {request.user} NO es el catedrático del curso.")

    # Verificar si el usuario está inscrito al curso en la tabla LineaPedido
    es_estudiante = LineaPedido.objects.filter(user=request.user, producto_id=curso.id).exists()

    # Si el usuario es catedrático y envía las notas a través del formulario
    if es_catedratico and request.method == "POST":
        for key, value in request.POST.items():
            # Verificar si es el campo zona o final
            if key.startswith("zona_") or key.startswith("final_"):
                linea_pedido_id = key.split("_")[1]  # Obtener el ID de la línea de pedido
                try:
                    # Buscar la línea de pedido correspondiente al estudiante
                    linea_pedido = LineaPedido.objects.get(id=linea_pedido_id)
                    # Actualizar la zona o la nota final
                    if key.startswith("zona_"):
                        linea_pedido.zona = int(value)
                    elif key.startswith("final_"):
                        linea_pedido.final = int(value)
                    # Guardar los cambios
                    linea_pedido.save()
                except LineaPedido.DoesNotExist:
                    # Manejar el caso de que no exista la línea de pedido
                    pass

    # Obtener la lista de estudiantes inscritos en el curso
    estudiantes_asignados = LineaPedido.objects.filter(producto=curso)

    # Si es catedrático o estudiante, renderizar la página del curso
    if es_catedratico or es_estudiante:
        return render(request, "inventario/curso_page.html", {
            "curso": curso,
            "es_catedratico": es_catedratico,  # Indicar si es catedrático
            "estudiantes_asignados": estudiantes_asignados,  # Enviar la lista de estudiantes asignados
        })
    else:
        return HttpResponseForbidden("No tienes acceso a este curso.")

    
@login_required
def exportar_notas_excel(request, id):
    # Obtener el curso específico
    curso = get_object_or_404(articulos, pk=id)

    # Verificar si el usuario es el catedrático del curso
    if request.user != curso.catedratico.user:
        return HttpResponseForbidden("No tienes permiso para descargar las notas de este curso.")

    # Crear un nuevo archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Notas de {curso.nombre}"

    # Agregar encabezados
    ws.append(['Estudiante', 'Zona (75pts)', 'Final (25pts)', 'Total'])

    # Obtener los estudiantes inscritos en el curso y sus notas
    lineas_pedido = LineaPedido.objects.filter(producto=curso)

    for linea in lineas_pedido:
        # Si los valores de zona o final están en None, los mostramos como 'N/A'
        zona = linea.zona if linea.zona is not None else 'N/A'
        final = linea.final if linea.final is not None else 'N/A'
        total = zona + final if isinstance(zona, int) and isinstance(final, int) else 'N/A'
        
        ws.append([linea.user.username, zona, final, total])

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Notas_{curso.nombre}.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)

    return response

@login_required
def desasignar_curso(request, id):
    # Obtener el curso específico
    curso = get_object_or_404(articulos, pk=id)

    # Verificar si el usuario está inscrito en el curso
    linea_pedido = get_object_or_404(LineaPedido, user=request.user, producto=curso)

    # Solo permitir que el estudiante se desasigne
    if request.user != linea_pedido.user:
        return HttpResponseForbidden("No tienes permiso para desasignarte de este curso.")

    # Eliminar la asignación
    linea_pedido.delete()

    # Aumentar la cantidad del artículo (curso) en 1, devolviendo el cupo
    curso.cantidad += 1
    curso.save()

    return redirect('perfil')
