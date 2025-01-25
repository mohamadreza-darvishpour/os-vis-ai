from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50)  # Example: "10 weeks"
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"