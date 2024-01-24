from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Trivia(models.Model):
    question = models.CharField(max_length=800)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserScores(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_scores(sender, instance, created, **kwargs):
    if created:
        UserScores.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_scores(sender, instance, **kwargs):
    UserScores.objects.get_or_create(user=instance)
    instance.userscores.save()