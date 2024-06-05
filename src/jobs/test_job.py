from apscheduler.schedulers.background import BackgroundScheduler

from functions.test_tasks import run_render

scheduler = BackgroundScheduler()

# assigning job to scheduler
scheduler.add_job(run_render, "interval", seconds=840)
