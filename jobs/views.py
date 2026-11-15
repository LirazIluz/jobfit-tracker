from rest_framework import viewsets
from .models import JobApplication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .analyzer import find_location, find_job_type, find_skills, fit_score, MY_SKILLS
from rest_framework import generics
from .serializers import JobApplicationSerializer, AnalyzeSerializer
from django.shortcuts import render
from .ai_analyzer import analyze_with_ai


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class AnalyzeView(generics.GenericAPIView):
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


def home(request):
    return render(request, "jobs/index.html")


class AnalyzeAIView(generics.GenericAPIView):
    serializer_class = AnalyzeSerializer

    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response(
                {"error": "text is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = analyze_with_ai(text)                                 
        except Exception as e:
            return Response(
                {"error": f"AI analysis failed: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(result)