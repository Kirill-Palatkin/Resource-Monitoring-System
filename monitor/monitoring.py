from datetime import timedelta
from django.utils import timezone
from .models import Incident, MachineMetric


def check_cpu_incident(machine):
    last_metric = MachineMetric.objects.filter(machine=machine).order_by('-timestamp').first()
    if not last_metric:
        return

    active_incident = Incident.objects.filter(
        machine=machine,
        incident_type=Incident.TYPE_CPU,
        end_time__isnull=True
    ).first()

    if last_metric.cpu > 85:
        if not active_incident:
            Incident.objects.create(
                machine=machine,
                incident_type=Incident.TYPE_CPU,
                description="CPU > 85%"
            )
    else:
        if active_incident:
            active_incident.end_time = timezone.now()
            active_incident.save()


def check_mem_incident(machine):
    threshold = 90.0
    duration = timedelta(minutes=30)
    now = timezone.now()

    metrics = MachineMetric.objects.filter(
        machine=machine,
        timestamp__gte=now - duration
    )
    if not metrics.exists():
        return

    active_incident = Incident.objects.filter(
        machine=machine,
        incident_type=Incident.TYPE_MEM,
        end_time__isnull=True
    ).first()

    if all(m.mem > threshold for m in metrics):
        if not active_incident:
            Incident.objects.create(
                machine=machine,
                incident_type=Incident.TYPE_MEM,
                description="Memory > 90% for 30 minutes"
            )
    else:
        if active_incident:
            active_incident.end_time = now
            active_incident.save()


def check_disk_incident(machine):
    threshold = 95.0
    duration = timedelta(hours=2)
    now = timezone.now()

    metrics = MachineMetric.objects.filter(
        machine=machine,
        timestamp__gte=now - duration
    )
    if not metrics.exists():
        return

    active_incident = Incident.objects.filter(
        machine=machine,
        incident_type=Incident.TYPE_DISK,
        end_time__isnull=True
    ).first()

    if all(m.disk > threshold for m in metrics):
        if not active_incident:
            Incident.objects.create(
                machine=machine,
                incident_type=Incident.TYPE_DISK,
                description="Disk > 95% for 2 hours"
            )
    else:
        if active_incident:
            active_incident.end_time = now
            active_incident.save()
