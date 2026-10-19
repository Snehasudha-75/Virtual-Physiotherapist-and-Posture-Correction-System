
from django.db import models
from django.contrib.auth.models import User



class HealthCondition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100)
    pain_level = models.IntegerField(default=1)  # 1: No pain, 2: Some pain, 3: Full pain

    def __str__(self):
        return f"{self.user.username} - {self.condition} (Level {self.pain_level})"
    

class SessionFeedback(models.Model):
    CONDITION_CHOICES = [
        ('back', 'Back'),
        ('elbow', 'Elbow'),
        ('neck', 'Neck'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)  # back / elbow / neck
    posture_score = models.IntegerField()
    pain_level = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.condition} - Pain {self.pain_level}"


class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('back', 'Back Pain'),
        ('elbow', 'Elbow Pain'),
        ('neck', 'Neck Pain'),
    ]
    
    PAIN_LEVELS = [
        (1, 'Level 1 - Low Pain'),
        (2, 'Level 2 - Moderate Pain'),
        (3, 'Level 3 - High Pain'),
    ]

    name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    pain_level = models.IntegerField(choices=PAIN_LEVELS, default=1)
    description = models.TextField()
    duration_minutes = models.IntegerField(default=5)
    instructions = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    gif_file = models.FileField(upload_to='exercises/gifs/', blank=True, null=True, help_text='Upload a GIF file for this exercise')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['exercise_type', 'pain_level', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_exercise_type_display()}"
