from apscheduler.schedulers.background import BackgroundScheduler
from snapshot.database import DatabaseWrapper, get_workspaces
from snapshot.slack import post_message
from snapshot.command import gm_week_command


def gm_week():
    workspaces = get_workspaces()
    for workspace in workspaces:
        db = DatabaseWrapper(workspace["team_id"])

        champion = db.get_last_weeks_winner()
        text = gm_week_command(champion)

        post_message(text, workspace["channel"], workspace["oauth"])


def tester():
    print("Test")


def setup_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(gm_week, "cron", day_of_week="0", hour="21", minute="39")
    scheduler.add_job(tester, "cron", second="*/10")
    scheduler.start()

