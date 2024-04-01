from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .views import import_asset


def start():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @scheduler.scheduled_job('cron', second='0', name='import_asset')
    def auto_check():
        print('is scheduled job')
        import_asset()

    scheduler.start()
