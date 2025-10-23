from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('api/', include('productos.urls')),  # Mantener compatibilidad con /api/
    path('', RedirectView.as_view(url='/productos/', permanent=False)),
]