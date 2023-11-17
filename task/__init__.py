default_app_config = 'task.apps.TaskConfig'

from django.db.utils import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler
from .models import TaskStatus, Task, RSSTask
from task.utils.scheduler import add_job, monitor
import logging
scheduler = BackgroundScheduler()

logger = logging.getLogger('main')

def start_tasks():
    try:
        tasks_to_start = TaskStatus.objects.filter(task_status=0)
        logger.info('拉取成功，下次60分启动')
        for task_status in tasks_to_start:
            if task_status.task_type == 'html':
                task = Task.objects.get(id=task_status.task_id)
                add_job(task.id, task.frequency, type='html')
            elif task_status.task_type == 'rss':
                task = RSSTask.objects.get(id=task_status.task_id)
                add_job(task.id, task.frequency, type='rss')

    except OperationalError:
        print('数据库尚未准备好')
        pass


# 在Django应用启动时调用
scheduler.add_job(
    start_tasks,
    'interval',
    minutes=60,  # 每隔4小时运行一次
)
scheduler.start()
