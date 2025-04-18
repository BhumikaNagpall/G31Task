from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey('main.AppUser', on_delete=models.CASCADE,null=True)
    # user = models.OneToOneField('main.AppUser', on_delete=models.CASCADE) 
    id = models.AutoField(primary_key=True)
    task_title = models.CharField(unique=True,max_length=30)
    task_description = models.TextField(max_length=100)
    TASK_PRIORITY_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
    ]
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed")],
        default="Pending"
    )

    task_priority = models.CharField(max_length=10, choices=TASK_PRIORITY_CHOICES, default='Medium')
    progress = models.PositiveIntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    class Meta:
        permissions = [
            # ("view_task", "Can view task"),
            ("edit_task", "Can edit task"),
            # ("delete_task", "Can delete task"),
        ]
    
    def __str__(self):
        return f"Task Title is: {self.task_title}, Task Description is: {self.task_description}"

