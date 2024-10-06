from xml.dom.minidom import Document
from django.urls import path
from inventario import views
from django.conf import settings
from django.conf.urls.static import static
from .views import catalogo, single_product, curso_page
from .views import exportar_notas_excel

urlpatterns = [
    path('', views.catalogo, name="Catalogo"),
    path('producto/<int:id>', views.single_product, name="Producto"),
    path('curso/<int:id>/', curso_page, name='curso_page'),
    path('curso/<int:id>/exportar-notas/', exportar_notas_excel, name='exportar_notas_excel'),
    path('desasignar-curso/<int:id>/', views.desasignar_curso, name='desasignar_curso'),
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)