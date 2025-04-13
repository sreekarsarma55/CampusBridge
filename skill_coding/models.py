from django.db import models
from django.conf import settings

class CodingTrack(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

class CodingProblem(models.Model):
    track = models.ForeignKey(CodingTrack, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=100)
    description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    expected_output = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    submitted_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"

class UserTrackProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(CodingTrack, on_delete=models.CASCADE)
    completed_problems = models.ManyToManyField(CodingProblem, blank=True)
    score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.track.title}"
