from django.contrib import admin
from .models import Machine, MachineMetric, Incident

admin.site.register(Machine)
admin.site.register(MachineMetric)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Incident._meta.fields]
    list_display = ['id', 'machine', 'incident_type', 'start_time', 'end_time']
    actions = ['delete_selected']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

