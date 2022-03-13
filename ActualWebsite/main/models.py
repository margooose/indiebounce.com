import django
from django.db import models
from accounts.models import Account
from django.core.validators import FileExtensionValidator
import hashlib

class Game(models.Model):
    STR = 'Strategy'
    ACT = 'Action'
    ADV = 'Adventure'

    GENRE_CHOICES = (
        (STR, 'Strategy'),
        (ACT, 'Action'),
        (ADV, 'Adventure')
    )

    def get_user_public_hash(self):  # change variable names
        str_pk_encoded = (str(self.pk)).encode()
        user_pk_hashed = hashlib.sha224(str_pk_encoded, usedforsecurity=True)
        user_public_hash = user_pk_hashed.hexdigest()
        return user_public_hash

    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    pub_date = models.DateField(default=django.utils.timezone.now)
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="game", null=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default=ADV)
    game_public_hash = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __int__(self):
        return self.pk


class GameSegment(models.Model):
    TD = 'Tower Defense'
    RTS = 'Real-Time Strategy'
    TBS = 'Turn-Based Strategy'
    DB = 'Deck-Building'
    VSM = 'Vehicle Simulator'
    CSM = 'Business Simulator'
    PUZ = 'Puzzle'

    STH = 'Stealth'
    SURV = 'Survival'
    ODP = '2-Dimensional Platformer'
    EDP = '3-Dimensional Platformer'
    FPS = 'Shooters'
    SPRT = 'Sports'
    RCE = 'Racing'

    HOR = 'Horror'
    PNT = 'Point & Click'
    ROUG = 'Rougelike'
    RPG = 'Role Playing Game'
    MON = 'Monster Tamer'

    GENRE_CHOICES = [
        ('Strategy', (  # thinky games
            (TD, 'Tower Defense'),
            (RTS, 'Real-Time Strategy'),
            (TBS, 'Turn-Based Strategy'),
            (DB, 'Deck-Building'),
            (VSM, 'Vehicle Simulator'),
            (CSM, 'Business Simulator'),
            (PUZ, 'Puzzle'),
        )),
        ('Action', (  # reflexy games
            (STH, 'Stealth'),
            (SURV, 'Survival'),
            (ODP, '2-Dimensional Platformer'),
            (EDP, '3-Dimensional Platformer'),
            (FPS, 'Shooter'),
            (SPRT, 'Sports'),
            (RCE, 'Racing'),
        )),
        ('Adventure', (  # explorery games
            (HOR, 'Horror'),
            (PNT, 'Point & Click'),
            (ROUG, 'Rougelike'),
            (RPG, 'Role Playing Game'),
            (MON, 'Monster Tamer'),
        ))
    ]

    def get_upload_location(self, filename):
        username_str = f'accounts/{str(self.game.account.password)}/{str(self.game.pk)}/{str(self.pk)}/{filename}'
        return username_str

    def get_user_public_hash(self):  # change variable names
        str_pk_encoded = (str(self.pk)).encode()
        user_pk_hashed = hashlib.sha1(str_pk_encoded, usedforsecurity=True)
        user_public_hash = user_pk_hashed.hexdigest()
        return user_public_hash

    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_upload_location, default=None, max_length=1024)
    html_file = models.FileField(upload_to=get_upload_location, validators=[FileExtensionValidator(['html'])], default=None, max_length=1024)
    folder = models.FileField(upload_to=get_upload_location, default=None, blank=True, max_length=1024)  # optional
    pub_date = models.DateField(default=django.utils.timezone.now)
    views = models.PositiveIntegerField(default=0)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default=PUZ)
    average_retention_time = models.PositiveIntegerField(default=0, null=True)
    is_complete = models.BooleanField(default=False)
    gamesegment_public_hash = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __int__(self):
        return self.pk

    def get_session_time(self, larger_value, session_time=[]):

        session_time.append(int(larger_value))
        if len(session_time) == 2:
            time_spent_on_site = abs(session_time[0] - session_time[1])
            if time_spent_on_site <= 5:
                session_time.clear()
                return None
            elif time_spent_on_site <= 900:
                session_time.clear()
                return abs(time_spent_on_site)
            else:
                session_time.clear()
                return 900
        else:
            pass

    def average_session_times(self, smol_value, all_session_times=[]):

        all_session_times.append(int(smol_value))
        return sum(all_session_times) / len(all_session_times)


