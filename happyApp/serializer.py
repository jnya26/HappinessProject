from .models import UserModel, TeamsModel, HappyModel
from rest_framework import serializers


class UserSterializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'password']


class UserMemmberSterializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['team_id']


class UserMoodSterializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['avarage_mood_mark']


class TeamSterializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsModel
        fields = ['team_name', 'logo']


class TeamMoodSterializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsModel
        fields = ['team_mood_rate']


class HappySterializer(serializers.ModelSerializer):
    class Meta:
        model = HappyModel
        fields = ['mood_mark']
