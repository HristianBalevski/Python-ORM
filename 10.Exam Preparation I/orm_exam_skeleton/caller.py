import os
import django


# Set up Django
from django.db.models import Q, Count, Prefetch, Avg, F

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    directors_query = Q()

    if search_name:
        directors_query &= Q(full_name__icontains=search_name)
    if search_nationality:
        directors_query &= Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(directors_query).order_by('full_name')

    output = []

    if not directors:
        return ""

    for d in directors:
        output.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")

    return '\n'.join(output)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if top_director:
        return f"Top Director: {top_director.full_name}, movies: {top_director.num_of_movies}."

    return ""


def get_top_actor():

    top_actor = Actor.objects.annotate(num_of_movies=Count('movies')).order_by('-num_of_movies', 'full_name').first()

    if top_actor:
        movie_titles = [movie.title for movie in top_actor.movies.only('title')]

        if movie_titles:
            avg_rating = top_actor.movies.aggregate(avg_rating=Avg('rating'))['avg_rating']

            result = (
                f"Top Actor: {top_actor.full_name}, "
                f"starring in movies: {', '.join(movie_titles)}, "
                f"movies average rating: {avg_rating:.1f}"
            )
            return result

    return ""


def get_actors_by_movies_count():

    top_actors = Actor.objects.annotate(num_of_movies=Count('actor_movies')).order_by('-num_of_movies', 'full_name')[:3]

    if not top_actors or top_actors[0].num_of_movies == 0:
        return ""

    output = []

    for a in top_actors:
        output.append(f"{a.full_name}, participated in {a.num_of_movies} movies")

    return '\n'.join(output)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if top_movie is None:
        return ""

    title = top_movie.title
    rating = f'{top_movie.rating:.1f}'
    starring_actor_name = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    cast = ', '.join(sorted([actor.full_name for actor in top_movie.actors.all()]))

    result = f"Top rated awarded movie: {title}, rating: {rating}. Starring actor: {starring_actor_name}. Cast: {cast}."

    return result


def increase_rating():
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if movies_to_update.exists():
        movies_to_update.update(rating=F('rating') + 0.1)
        return f"Rating increased for {movies_to_update.count()} movies."
    else:
        return "No ratings increased."