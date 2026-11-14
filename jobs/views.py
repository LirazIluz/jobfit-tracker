from rest_framework import viewsets
from .models import JobApplication
from .serializers import JobApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .analyzer import find_location, find_job_type, find_skills, fit_score, MY_SKILLS
from rest_framework import generics
from .serializers import JobApplicationSerializer, AnalyzeSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class AnalyzeView(APIView):
    serializer_class = AnalyzeSerializer
    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response(
                {"error": "text is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        skills = find_skills(text)
        missing = []
        for skill in skills:
            if skill not in MY_SKILLS:
                missing.append(skill)
        
        return Response({
            "location": find_location(text),         
            "job_type": find_job_type(text),         
            "skills_found": skills,
            "skills_missing": missing,
            "fit_score": fit_score(skills),        
        })