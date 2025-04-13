from django import forms
from .models import CodingTrack, CodingProblem

class CodingTrackForm(forms.ModelForm):
    class Meta:
        model = CodingTrack
        fields = ['title', 'description', 'difficulty']

class CodingProblemForm(forms.ModelForm):
    class Meta:
        model = CodingProblem
        fields = ['title', 'description', 'sample_input', 'sample_output', 'expected_output', 'difficulty']
