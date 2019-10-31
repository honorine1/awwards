from rest_framework import serializers
from .models import Projects,Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'contact','user')

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('proTitle', 'proImage', 'proDesc','proLink','profile','user','posted_date')
