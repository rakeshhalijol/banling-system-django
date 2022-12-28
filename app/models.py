from django.db import models

# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Count(models.Model):
    user = models.ForeignKey(Person,on_delete=models.CASCADE)
    amount = models.FloatField(default=100000)

    def __str__(self):
       return f"{self.user}"

