from apscheduler.schedulers.background import BackgroundScheduler

from jobs.render_tasks import run_render

scheduler = BackgroundScheduler()

# assinging job to scheduler
scheduler.add_job(run_render, "interval", seconds=840)
