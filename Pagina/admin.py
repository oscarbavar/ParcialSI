from django.contrib import admin
from .models import Pagina

# Define admin actions here

class PaginaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )  
    
admin.site.register(Pagina, PaginaAdmin)
