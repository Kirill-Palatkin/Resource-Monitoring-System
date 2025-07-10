# Resource Monitoring System
Cистема для мониторинга метрик серверов

Автоматический сбор метрик (CPU, RAM и т.д.) с опросом каждые 15 мин (Celery Beat + Redis). Алёртинг при аномалиях + запись инцидентов в БД.

1. Сервер метрик (эмуляция 30 машин):
python mock_metrics.py

2. Django-сервер:
python manage.py runserver
Админка: http://localhost:8000/admin

3. MySQL Workbench:
Хост: 127.0.0.1
Порт: 3306

4. Redis (запускать с правами администратора):
redis-server

5. Celery Worker (запускать с правами администратора):
celery -A monitoring_project worker --loglevel=info --pool=solo

6. Celery Beat (запускать с правами администратора):
celery -A monitoring_project beat --loglevel=info

Каждый команда прописывается в отдельном терминале.
