from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def my_job():
    from . import views
    views.import_asset()


# 5분마다 my_job 함수 실행
scheduler.add_job(my_job, trigger='cron', hour='15', minute='35')
scheduler.start()
