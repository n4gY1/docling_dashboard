from django.contrib import admin
from django.contrib.admin import ModelAdmin

from dashboard.models import GeneratedRag

class GeneratedRagAdmin(ModelAdmin):
    list_display = ("filename","created_at","finished_at","errors")
    sortable_by = ["finished_at",]

# Register your models here.
admin.site.register(GeneratedRag,GeneratedRagAdmin)