import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai  # Gemini
from .gemini_helper import ask_gemini
import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import CodingTrack, CodingProblem, Submission
from .models import CodingTrack, CodingProblem
from .forms import CodingTrackForm, CodingProblemForm
from django.contrib.auth.decorators import login_required

genai.configure(api_key="AIzaSyBF_if642BpoY1mWeo_sA2fvHjMaIGwxv8")
@login_required
def track_list(request):
    tracks = CodingTrack.objects.all()
    return render(request, 'users/track_list.html', {'tracks': tracks})

@login_required
def track_detail(request, track_id):
    track = get_object_or_404(CodingTrack, id=track_id)
    problems = track.problems.all()
    return render(request, 'users/track_detail.html', {
        'track': track,
        'problems': problems
    })

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    return render(request, 'users/problem_detail.html', {
        'problem': problem
    })

@login_required
def submit_code(request, problem_id):
    if request.method == 'POST':
        code = request.POST.get('code')
        # Placeholder for evaluation logic
        problem = get_object_or_404(CodingProblem, id=problem_id)
        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            is_correct=False  # Update after evaluating
        )
        return redirect('skill_coding:problem_detail', problem_id=problem_id)

@login_required
def add_track(request):
    if not request.user.is_faculty:  # Check if the user is Faculty (admin role)
        return HttpResponseForbidden("You are not authorized to add tracks.")
    
    if request.method == 'POST':
        form = CodingTrackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skill_coding:track_list')  # Redirect to the track list page
    else:
        form = CodingTrackForm()
    
    return render(request, 'users/add_track.html', {'form': form})

@login_required
def add_problem(request, track_id):
    if not request.user.is_faculty:  # Check if the user is Faculty
        return HttpResponseForbidden("You are not authorized to add problems.")
    
    track = get_object_or_404(CodingTrack, id=track_id)
    
    if request.method == 'POST':
        form = CodingProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.track = track
            problem.save()
            return redirect('skill_coding:track_detail', track_id=track.id)  # Redirect to track detail page
    else:
        form = CodingProblemForm()
    
    return render(request, 'users/add_problem.html', {'form': form, 'track': track})

@login_required
def faculty_dashboard(request):
    tracks = CodingTrack.objects.all()
    if request.user.role=='student':
        return render(request, 'users/track_list.html', {'tracks': tracks})
    elif request.user.role=='faculty':
        return render(request, 'users/faculty_dashboard.html', {'tracks': tracks})
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")
    

@login_required
def submit_code(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    output = None
    error = None
    verdict = None

    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')


        input_data = problem.sample_input
        
        language_versions = {
            "python3": "3",     # Python 3
            "cpp": "5",         # C++
            "java": "4",        # Java
            "c": "5",           # C
            "javascript": "4",  # JavaScript
        }
        version_index = language_versions.get(language, "0")

        payload = {
            "clientId": settings.JDOODLE_CLIENT_ID,
            "clientSecret": settings.JDOODLE_CLIENT_SECRET,
            "script": code,
            "language": language,
            "versionIndex": version_index,
            "stdin": input_data
        }

        response = requests.post("https://api.jdoodle.com/v1/execute", json=payload)
        if response.status_code == 200:
            result = response.json()
            output = result.get("output", "").strip()
            expected_output = problem.expected_output.strip()

            is_correct = output == expected_output
            verdict = "Correct ✅" if is_correct else "Incorrect ❌"

            Submission.objects.create(
                user=request.user,
                problem=problem,
                submitted_code=code,
                is_correct=is_correct,
                score=10 if is_correct else 0
            )
        else:
            output = "Error executing code."
            verdict = "❌ Error"
            error

        return render(request, 'users/problem_detail.html', {
            'problem': problem,
            'output': output,
            'verdict': verdict,
            'submitted_code': code
        })


    return render(request, 'users/problem_detail.html', {
        'problem': problem
    })


@login_required
def submission_history(request):
    submissions = Submission.objects.filter(user=request.user).select_related('problem').order_by('-submitted_at')
    return render(request, 'users/submission_history.html', {
        'submissions': submissions
    })



@csrf_exempt
def ask_assistant(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        response = ask_gemini(prompt)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)