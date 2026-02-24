import logging
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from news.digest import send_weekly_digest

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone="UTC")
        scheduler.add_jobstore(DjangoJobStore(), "default")

        @util.close_old_connections
        def job():
            send_weekly_digest()

        # Например: каждый понедельник в 09:00 UTC
        # (если хочешь по NY — можно поставить timezone="America/New_York")
        scheduler.add_job(
            job,
            trigger=CronTrigger(day_of_week="mon", hour=9, minute=0),
            id="weekly_digest",
            max_instances=1,
            replace_existing=True,
        )

        # Чистка истории запусков, иначе таблица логов будет расти
        scheduler.add_job(
            util.delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour=9, minute=5),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
            kwargs={"max_age": 60 * 60 * 24 * 30},  # 30 дней
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()