from django.contrib import admin
from ner import models

# Register your models here.


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color']
    search_fields = ('name', )

    class Meta:
        model = models.Label


class LabelProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'creator']
    ordering = ('-create_time',)
    search_fields = ('project',)

    class Meta:
        model = models.LabelProject


admin.site.register(models.Label, LabelAdmin)
admin.site.register(models.LabelProject, LabelProjectAdmin)