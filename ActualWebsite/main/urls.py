from django.urls import path
from . import views
app_name = 'main'
# we start our views here in urls, passes to views
urlpatterns = [

    path('game/', views.game, name='game'),

    # main
    path('', views.home, name="home"),
    path('game=<str:game_public_hash>/', views.playGame, name="playGame"),
    path('gamesegment=<str:gamesegment_public_hash>/', views.playGameSegment, name="playGameSegment"),
    path('recent/', views.recent, name='recent'),
    path('genre=<str:genre>/', views.SpecificGenre, name='specificGenre'),
    path('user=<str:user_public_hash>/', views.viewUser, name='viewUser'),

    # documentation
    path('help/', views.help, name="help"),
    path('cookiepolicy', views.cookiePolicy, name="cookiePolicy"),
    path('privacypolicy/', views.privacyPolicy, name="privacyPolicy"),
    path('updatelog/', views.updateLog, name='updateLog'),

    # account
    path('account/', views.account, name="account"),
    path('account/games/', views.accountGames, name="accountGame"),
    path('account/game=<str:game_public_hash>/', views.accountSpecificGame, name="accountSpecificGame"),
    path('account/gamesegment=<str:gamesegment_public_hash>/', views.accountSpecificGameSegment, name='AccountSpecificGameSegment'),

    # registration
    path('register/', views.register, name="register"),
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),

]