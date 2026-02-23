from apscheduler.schedulers.background import BackgroundScheduler

from src.functions.test_tasks import run_test

scheduler = BackgroundScheduler()

# assigning job to scheduler
scheduler.add_job(run_test, "interval", seconds=840)
