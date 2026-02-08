from django.db import models
from django.conf import settings

class SleepLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    quality = models.IntegerField(choices=[(i, i) for i in range(1, 11)], default=7)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes}m"
