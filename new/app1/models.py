from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
  Name=models.CharField(max_length=77)
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  phone_no=models.CharField(max_length=10)
  country=models.CharField(max_length=33)

  def __str__(self):
   return f"{self.Name}"






class Student(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name