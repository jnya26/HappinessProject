from datetime import datetime

from django.db.models import Avg
from django.http import Http404
from rest_framework import views, status, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from .models import UserModel, TeamsModel, HappyModel
from .serializer import UserSterializer, TeamSterializer, HappySterializer, UserMemmberSterializer, \
    TeamMoodSterializer, UserMoodSterializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from config import settings


# Create your views here.

class Users(views.APIView):
    """"GET/http://127.0.0.1:8000/users/ - get all users"""""

    # permission_classes = [IsAuthenticated]
    def get(self, request):
        users = UserModel.objects.all()
        users_serializer = UserSterializer(users, many=True)
        return Response(users_serializer.data)

    """POST/http://127.0.0.1:8000/users/ - create a new user"""

    def post(self, request):

        serializer = UserSterializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user.token_id = token
            user.save()

            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class User(views.APIView):
    def get_or_404(self, pk):
        try:
            user = UserModel.objects.get(pk=pk)
            return user
        except UserModel.DoesNotExist:
            return Http404

    """GET/http://127.0.0.1:8000/user/<id> - get an exactly user(using id)"""

    def get(self, request, pk):
        user = self.get_or_404(pk=pk)
        serializer = UserSterializer(instance=user)
        return Response(serializer.data)

    """ PUT/http://127.0.0.1:8000/user/<id> - change an exactly user(using id)"""

    def put(self, request, pk):
        user = self.get_or_404(pk=pk)
        serializer = UserSterializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ DELETE/http://127.0.0.1:8000/user/<id> - delete an exactly user(using id) """

    def delete(self, request, pk):
        user = self.get_or_404(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Happy(views.APIView):
    MARK_VALUE_NUMERIC = [1, 2, 3, 4, 5, 6, 7]
    def get_or_404(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
            return user
        except UserModel.DoesNotExist:
            return Http404

    """POST/http://127.0.0.1:8000/user/<id>/happiness - choose your mood for today(using id)"""

    def post(self, request, user_id):
        user = self.get_or_404(user_id=user_id)
        serializer = HappySterializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['mood_mark'] in self.MARK_VALUE_NUMERIC:
                day = str(datetime.today().strftime('%Y-%m-%d'))
                day_in_db = HappyModel.objects.filter(day=day, user_id=user).exists()
                if day_in_db:
                    return Response('You have been calculated on this day')
                else:
                    serializer.save(user_id=user)
                    value= round(serializer.data['mood_mark']) - 1
                    return Response(settings.MARK_VALUE[value], status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """GET/http://127.0.0.1:8000/user/<id>/happiness - get your average mood for all period(using id) and save in db"""

    def get(self, request, user_id):
        user = self.get_or_404(user_id=user_id)
        instence = HappyModel.objects.filter(user_id=user)
        print(instence)
        if instence.exists():
            average_mark = instence.aggregate(Avg('mood_mark'))['mood_mark__avg']
            user.avarage_mood_mark = average_mark
            serializer = UserMoodSterializer(data={'avarage_mood_mark': user.avarage_mood_mark}, instance=user)
            if serializer.is_valid():
                serializer.save()
                average_mark=round(average_mark)-1
                return Response(settings.MARK_VALUE[average_mark], status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
GET/http://127.0.0.1:8000/team/ - list of all teams
POST/http://127.0.0.1:8000/team/ -create a new team
GET/http://127.0.0.1:8000/team/<team.id>/ - get a team with team.id
PUT/http://127.0.0.1:8000/team/<team.id>/ - change a team with team.id
DELETE/http://127.0.0.1:8000/team/<team.id>/ - remove a team with team.id
"""


class Teams(viewsets.ModelViewSet):
    serializer_class = TeamSterializer
    queryset = TeamsModel.objects.all()


"""GET/http://127.0.0.1:8000/team/<team.id>/memmbers/ - get all members with team.id"""


class TeamRedactor(views.APIView):
    def get_or_404(self, id):
        try:
            team = TeamsModel.objects.get(id=id)
            return team
        except UserModel.DoesNotExist:
            return Http404

    def get(self, request, id):
        team = self.get_or_404(id=id)
        team_users = UserModel.objects.filter(team_id=team)
        serializer = UserSterializer(team_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""POST/http://127.0.0.1:8000/team/<team.id>/memmbers/<user.id>/ - add memmber in team with team.id
   PUT/http://127.0.0.1:8000/team/<team.id>/memmbers/<user.id>/ - remove memmber from team with team.id
"""


class AddTeamMemmber(views.APIView):

    def get_or_404(self, id):
        try:
            team = TeamsModel.objects.get(id=id)
            return team
        except UserModel.DoesNotExist:
            return Http404

    def post(self, request, id, pk):
        team = self.get_or_404(id=id)
        user = UserModel.objects.get(pk=pk)
        user.team_id = team.id
        serializer_user = UserMemmberSterializer(data=request.data, instance=user)
        if serializer_user.is_valid():
            serializer_user.save()
            return Response(serializer_user.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, pk):
        user = UserModel.objects.get(pk=pk)
        user.team_id = None
        serializer_user = UserMemmberSterializer(data={'team_id': user.team_id}, instance=user)
        if serializer_user.is_valid():
            serializer_user.save()
            return Response(serializer_user.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamMoodMark(views.APIView):
    """"PUT/http://127.0.0.1:8000/team/<team.id>>/mood_mark/ - calculate avarage Mood-rate for team using team.id
    """""

    def get_or_404(self, id):
        try:
            team = TeamsModel.objects.get(id=id)
            return team
        except UserModel.DoesNotExist:
            return Http404

    def put(self, request, id):
        team = self.get_or_404(id=id)
        users = UserModel.objects.filter(team_id=team.id)
        instense = users.aggregate(Avg('avarage_mood_mark'))['avarage_mood_mark__avg']
        print(instense)
        team.team_mood_rate = instense
        serializer = TeamMoodSterializer(data={'team_mood_rate': team.team_mood_rate}, instance=team)
        if serializer.is_valid():
            serializer.save()
            if instense is not None:
                value = round(instense) - 1
                print(value)
                return Response(settings.MARK_VALUE[value], status=status.HTTP_200_OK)
            else:
                return Response('Teammembers did not put happiness yet.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""""GET/http://127.0.0.1:8000/teams/mood_mark/ - calculate avarage Mood-rate for all teams
"""""


class TeamsMoodMark(views.APIView):
    def get(self, request):
        teams = TeamsModel.objects.all()
        instense = teams.aggregate(Avg('team_mood_rate'))['team_mood_rate__avg']
        if instense is not None:
            value = round(instense) - 1
            return Response(settings[value], status=status.HTTP_200_OK)
        else:
            return Response("Happiness for all team is empty")


class SuperuserOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
