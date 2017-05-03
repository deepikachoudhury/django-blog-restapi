from django.contrib import admin

# Register your models here.
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ("title","created")
    #prepopulated_fields = {"slug" : ("title",)}

admin.site.register(Blog,BlogAdmin)