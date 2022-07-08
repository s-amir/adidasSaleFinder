from django.db import models

class User(models.Model):
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=14)
    last_message_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name