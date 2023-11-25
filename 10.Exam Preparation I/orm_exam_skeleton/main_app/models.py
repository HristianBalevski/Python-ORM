from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import MainInfo, AwardAndUpdate


class Director(MainInfo):
    years_of_experience = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0)
    objects = DirectorManager()


class Actor(MainInfo, AwardAndUpdate):
    pass


class Movie(AwardAndUpdate):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action'
        COMEDY = 'Comedy'
        DRAMA = 'Drama'
        OTHER = 'Other'

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=6, choices=GenreChoices.choices, default=GenreChoices.OTHER)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='actor_movies')
