from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# making plan 
class Plan(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)#You can leave it blank.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_date = models.DateField()
    plan_time = models.TimeField(null=True, blank=True)# You can also not use time.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    result_note = models.TextField(blank=True, help_text="یادداشت کاربر در مورد نحوه انجام کار")

    def __str__(self):
        return self.title
    


#saving work for user

class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    success_percentage = models.PositiveIntegerField() #Success rate
    ai_feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.date} - {self.success_percentage}%"