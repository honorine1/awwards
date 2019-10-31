from django import forms
from .models import Profile,Projects,Comments


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['profile','user', 'posted_date','usability','content','design','vote_submissions']
        
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['project','user']
       

class VoteForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['proTitle','proImage','proDesc','proLink','profile','user','posted_date','vote_submissions']

