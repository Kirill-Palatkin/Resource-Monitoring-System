from django.db import models
from django.utils import timezone


class Machine(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()

    class Meta:
        unique_together = ('ip_address', 'port')

    def __str__(self):
        return f"{self.name} ({self.ip_address}:{self.port})"


class MachineMetric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.IntegerField()
    mem = models.FloatField()
    disk = models.FloatField()
    uptime = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        local_time = timezone.localtime(self.timestamp)
        return f"{self.machine} at {local_time:%Y-%m-%d %H:%M:%S}"


class Incident(models.Model):
    TYPE_CPU = 'cpu'
    TYPE_MEM = 'mem'
    TYPE_DISK = 'disk'
    TYPES = [
        (TYPE_CPU, 'CPU'),
        (TYPE_MEM, 'Memory'),
        (TYPE_DISK, 'Disk'),
    ]

    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=10, choices=TYPES)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('machine', 'incident_type', 'end_time')

    def __str__(self):
        status = 'active' if self.end_time is None else 'closed'
        return f'{self.machine} {self.incident_type} ({status})'
