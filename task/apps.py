from django.apps import AppConfig


class TaskConfig(AppConfig):
    name = 'task'
    verbose_name = '任务管理'

    def ready(self):
        try:
            from .models import TaskStatus, Task, RSSTask  # 导入任务模型
            from task.utils.scheduler import add_job

            tasks_to_start = TaskStatus.objects.filter(task_status=0)  # 获取所有应该运行的任务
            for task_status in tasks_to_start:
                # 获取与 TaskStatus 相关联的 Task 或 RSSTask 实例
                if task_status.task_type == 'html':
                    task = Task.objects.get(id=task_status.task_id)
                    add_job(task.id, task.frequency, type='html')
                elif task_status.task_type == 'rss':
                    task = RSSTask.objects.get(id=task_status.task_id)
                    add_job(task.id, task.frequency, type='rss')
                  

        except OperationalError:
            print('数据库尚未准备好')
            # 处理数据库尚未准备好的情况
            pass
