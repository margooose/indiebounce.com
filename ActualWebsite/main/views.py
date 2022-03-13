from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView

from .forms import GameCreationForm, GameSegmentCreationFormOne, GameSegmentCreationFormTwo, RegisterForm, ProfilePictureForm
from .models import Game, GameSegment
from accounts.models import Account
import datetime
import os


# Regular Functions

def get_time_in_seconds():
    current_time = datetime.datetime.now()
    hours = current_time.hour
    minutes = current_time.minute
    seconds = current_time.second
    current_time_calculated = seconds + (minutes * 60) + (hours * 60)
    return current_time_calculated


# Create your views here.

def home(request):

    # getting user recommended_gamesegments
    if request.user.is_authenticated:
        if request.user.preferred_genre is None:
            recommended_gamesegments = GameSegment.objects.order_by('average_retention_time')[:10]

        else:
            recommended_gamesegments = GameSegment.objects.filter(genre__startswith=request.user.preferred_genre).order_by(
                '-average_retention_time')[:10]

    elif request.COOKIES.get('preferred_genre'):
        recommended_gamesegments = GameSegment.objects.filter(
            genre__startswith=request.COOKIES.get('preferred_genre')).order_by('average_retention_time')[:10]

        if recommended_gamesegments is None:
            recommended_gamesegments = GameSegment.objects.order_by('average_retention_time')[:10]

    else:
        recommended_gamesegments = GameSegment.objects.order_by('average_retention_time')[:10]

    # checks if user agrees to cookies
    if request.COOKIES.get('agrees_to_cookies'):
        agrees_to_cookies = True
    else:
        agrees_to_cookies = False
        if request.method == 'POST':
            response = render(request, 'home.html', {'recommended_gamesegments': recommended_gamesegments, 'agrees_to_cookies': agrees_to_cookies})
            response.set_cookie('agrees_to_cookies', 'agrees_to_cookies')
            return response

    if request.method == "POST":

        request_scrollbar_location = request.POST.get('scrollbar_location', None)

        if request_scrollbar_location == 'commence_':
            pass

        return JsonResponse(request_scrollbar_location)

    context = {'recommended_gamesegments': recommended_gamesegments, 'agrees_to_cookies': agrees_to_cookies}
    return render(request, 'home.html', context)


def help(request):
    context = {}
    return render(request, 'documentation/help.html', context)


def cookiePolicy(request):
    context = {}
    return render(request, 'documentation/cookiePolicy.html', context)


def privacyPolicy(request):
    context = {}
    return render(request, 'documentation/privacyPolicy.html', context)


def account(request):
    if request.user.is_authenticated:
        account = request.user

        form = ProfilePictureForm(request.POST and request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():

                user_picture = request.FILES.get('user_picture')
                account.user_picture = user_picture
                account.has_user_picture = True
                account.save()
                print('seemed to save')

        context = {'account': account, 'form': form}
        return render(request, 'account settings/account profile.html', context)

    else:
        return HttpResponseRedirect(redirect_to='/login/')


def accountGames(request):
    if request.user.is_authenticated:
        account = request.user
        AccountGames = Game.objects.filter(account__username__contains=request.user.username).order_by('-pub_date')

        GameForm = GameCreationForm(request.POST or None)
        if request.method == 'POST':

            if '_delete' in request.POST:
                gamepk = request.POST.get('_delete')
                game = Game.objects.get(pk=gamepk)
                game.delete()

            if GameForm.is_valid():
                game = GameForm.save()
                game.account = request.user
                game.game_public_hash = game.get_user_public_hash()

                directory_name = game.pk
                os.mkdir('static/accounts/' + str(game.account.pk) + '/' + str(directory_name))

                game.save()
                return HttpResponseRedirect(redirect_to='')

        context = {'account': account, 'AccountGames': AccountGames, 'GameForm': GameForm}
        return render(request, 'account settings/account games.html', context)

    else:
        return HttpResponseRedirect(redirect_to='/login/')


def accountSpecificGame(request, game_public_hash):
    if request.user.is_authenticated:
        account = request.user
        game = Game.objects.get(game_public_hash=game_public_hash)
        gameGsegments = game.gamesegment_set.all().order_by('pub_date')
        if game.account == request.user:

            GsegmentForm = GameSegmentCreationFormOne(request.POST, request.FILES or None)
            if request.method == 'POST':

                if '_delete' in request.POST:
                    gsegmentpk = request.POST.get('_delete')
                    gsegment = GameSegment.objects.get(game_public_hash=gsegmentpk)
                    gsegment.delete()

                if GsegmentForm.is_valid():
                    gsegment = GsegmentForm.save(commit=False)
                    gsegment.game = game
                    gsegment.gamesegment_public_hash = gsegment.get_user_public_hash()
                    gsegment.save()

                    directory_name = gsegment.pk
                    os.mkdir('static/accounts/' + str(game.account.pk) + '/' + str(game.pk) + '/' + str(
                        directory_name))

                    return HttpResponseRedirect(
                        redirect_to='/account/gamesegment=' + str(gsegment.gamesegment_public_hash) + '/#Finish-Gsegment-Div')

            context = {'account': account, 'game': game, 'GsegmentForm': GsegmentForm, 'gameGsegments': gameGsegments}
            return render(request, 'account settings/account specific game.html', context)

        else:
            return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect(redirect_to='/login/')


def accountSpecificGameSegment(request, gamesegment_public_hash):
    if request.user.is_authenticated:
        account = request.user
        gsegment = GameSegment.objects.get(gamesegment_public_hash=gamesegment_public_hash)
        if gsegment.game.account != request.user:
            return HttpResponseRedirect(redirect_to='/')

        else:
            GsegmentForm = GameSegmentCreationFormTwo(request.POST, request.FILES or None)
            if request.method == 'POST':

                if '_delete' in request.POST:
                    gsegmentpk = request.POST.get('_delete')
                    gsegment = GameSegment.objects.get(gamesegment_public_hash=gsegmentpk)
                    gsegment.delete()

                if GsegmentForm.is_valid():

                    thumbnail = request.FILES.get('thumbnail')
                    html_file = request.FILES.get('html_file')

                    gsegment.thumbnail = thumbnail
                    gsegment.html_file = html_file
                    gsegment.is_complete = True

                    if request.FILES.get('folder'):
                        folder = request.FILES.get('folder')
                        gsegment.folder = folder

                    gsegment.save()

                    return HttpResponseRedirect(redirect_to='')

            context = {'account': account, 'gsegment': gsegment, 'GsegmentForm': GsegmentForm}
            return render(request, 'account settings/account specific gamesegment.html', context)

    else:
        return HttpResponseRedirect(redirect_to='/login/')


def register(request):
    form = RegisterForm(request.POST or None)

    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():

            account = form.save()

            account.user_public_hash = account.get_user_public_hash()

            directory_name = account.pk
            os.mkdir('static/accounts/' + str(directory_name))

            account.save()
            return HttpResponseRedirect(redirect_to='/login/')

    return render(request, 'registration/register.html', context)


def loginUser(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('login worked?')
                return HttpResponseRedirect(redirect_to='/')
            else:
                print("login didn't work")
    context = {'form': form}
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)

    context = {}
    return render(request, 'registration/logout.html', context)


def playGame(request, game_public_hash):
    game = Game.objects.get(game_public_hash=game_public_hash)
    gameGsegments = game.gamesegment_set.all().order_by('pub_date')

    context = {'game': game, 'gameGsegments': gameGsegments}
    return render(request, 'playGame.html', context)


def playGameSegment(request, gamesegment_public_hash):
    # this is firing whenever the event fires
    gsegment = GameSegment.objects.get(gamesegment_public_hash=gamesegment_public_hash)
    game = gsegment.game
    recommendedGsegments = GameSegment.objects.order_by('-views')[:10]
    context = {'gsegment': gsegment, 'game': game, 'recommendedGsegments': recommendedGsegments}

    #  tracks retention time
    if request.POST.get('userHidden') is not None:

        x = gsegment.get_session_time(larger_value=get_time_in_seconds())
        if x is None:
            pass
        elif x <= 10:
            gsegment.views -= 1
            gsegment.save()

        else:
            gsegment.average_retention_time = gsegment.average_session_times(smol_value=x)
            gsegment.save()

    elif request.POST.get('userVisible') is not None:
        pass
        # still not sure if this elif is necessary

    else:
        gsegment.views += 1
        gsegment.save()

        # cookies and setting user preferred_genre
        if request.user.is_authenticated:
            request.user.preferred_genre = gsegment.genre
            request.user.save()

        else:
            response = render(request, 'playGameSegment.html', context)
            response.set_cookie('preferred_genre', gsegment.genre)
            return response

    return render(request, 'playGameSegment.html', context)


def recent(request):
    recentGsegments = GameSegment.objects.order_by('-pub_date')[:10]

    context = {'recentGsegments': recentGsegments}
    return render(request, 'genres/recent.html', context)


def SpecificGenre(request, genre):
    genre = genre
    genreGsegments = GameSegment.objects.filter(genre__startswith=genre).order_by('-views')[:10]

    context = {'genreGsegments': genreGsegments, 'genre': genre}
    return render(request, 'genres/specificGenre.html', context)


def viewUser(request, user_public_hash):
    account = Account.objects.get(user_public_hash=user_public_hash)
    accountGameList = Game.objects.filter(account__user_public_hash=user_public_hash)

    context = {'account': account, 'accountGameList': accountGameList}
    return render(request, 'viewUser.html', context)
