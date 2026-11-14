from django.db import models
from .analyzer import find_location, find_job_type, find_skills, fit_score

class JobApplication(models.Model):
 
    class Status(models.TextChoices):
        SAVED = "SAVED", "Saved"
        APPLIED = "APPLIED", "Applied"
        INTERVIEW = "INTERVIEW", "Interview"
        REJECTED = "REJECTED", "Rejected"
        OFFER = "OFFER", "Offer"

    class JobType(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        PART_TIME = "PART_TIME", "Part-time"
        FULL_TIME = "FULL_TIME", "Full-time"
        INTERNSHIP = "INTERNSHIP", "Internship"

    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, blank=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
    cv_version = models.CharField(max_length=100, blank=True)
    applied_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    fit_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.title}"

    def save(self, *args, **kwargs):
        if self.description:
            if not self.location:
                self.location = find_location(self.description)
            if not self.job_type:
                self.job_type = find_job_type(self.description)   
            skills = find_skills(self.description)
            self.fit_score = fit_score(skills)        
        super().save(*args, **kwargs)
