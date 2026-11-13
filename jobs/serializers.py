from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"

    def validate(self, data):
        company = data.get("company", self.instance.company if self.instance else "")
        title = data.get("title", self.instance.title if self.instance else "")

        duplicates = JobApplication.objects.filter(
            company__iexact=company,      
            title__iexact=title,          
        )

        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)  

        if duplicates.exists():     
            raise serializers.ValidationError("You already saved this job!")

        return data