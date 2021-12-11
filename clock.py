from apscheduler.schedulers.blocking import BlockingScheduler
from .my_app.filmography.models import ActorUserRequest

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    api_requests = ActorUserRequest.objects.filter(status='p')
    if api_requests.exists():
        obj = api_requests.last()
        obj.set_response()
    print('This job is run every one minute.')


sched.start()