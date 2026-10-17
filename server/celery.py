# import os
# from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# celery_app = Celery("server")
# celery_app.config_from_object("django.conf:settings", namespace="CELERY")
# # find tasks with shared_task decorator in all registered Django app configs
# celery_app.autodiscover_tasks()