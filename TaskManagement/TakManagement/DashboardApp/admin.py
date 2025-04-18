from django.contrib import admin
from .models import Task
class TaskAdmin(admin.ModelAdmin):
    list_display=['id','task_title','task_description','task_priority','progress','start_date','end_date']
    list_filter=['task_title','id']
admin.site.register(Task,TaskAdmin)