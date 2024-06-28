from django.contrib import admin
from django.urls import path
from Pagina import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('iniciarsesion/', views.iniciarsesion, name='iniciarsesion'),
    path('registro/', views.registro, name='registro'),
    path('cerrarsesion/', views.cerrarsesion, name='cerrarsesion'),
    path('descripcion/', views.descripcion, name='descripcion'),
    path('product/crear/', views.crear, name='crear'),
    path('product/<int:product_id>/', views.detalle, name='detalle'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
