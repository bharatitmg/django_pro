from django.db import models
from django.contrib.auth.models import User

class RentalBoyfriendAndGirlfriend(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    price = models.TextField(blank=True)
    def __str__(self):
        return f"{self.id}: {self.name} ({self.get_gender_display()})"
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boyfriend_girlfriend = models.ForeignKey(RentalBoyfriendAndGirlfriend, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()  # You might want to use a rating scale (e.g., 1 to 5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.boyfriend_girlfriend.name}"