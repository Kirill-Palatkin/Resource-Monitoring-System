from celery import shared_task
import requests, logging
from .models import Machine, MachineMetric
from .monitoring import check_cpu_incident, check_mem_incident, check_disk_incident

log = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(requests.RequestException,),
             retry_backoff=True, retry_kwargs={"max_retries": 3})
def fetch_metrics(self):
    for machine in Machine.objects.all():
        try:
            resp = requests.get(f"http://{machine.ip_address}:{machine.port}/metrics", timeout=5)
            resp.raise_for_status()
            data = resp.json()

            mem  = float(data["mem"].rstrip("%"))
            disk = float(data["disk"].rstrip("%"))

            MachineMetric.objects.create(
                machine=machine,
                cpu=int(data["cpu"]),
                mem=mem,
                disk=disk,
                uptime=data["uptime"],
            )

            check_cpu_incident(machine)
            check_mem_incident(machine)
            check_disk_incident(machine)

        except Exception as exc:
            log.warning("Fetch failed for %s: %s", machine.ip_address, exc)
