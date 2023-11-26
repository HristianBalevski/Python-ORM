import os
import django
from django.db.models import Q, Count, Avg


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    author_query = Q()

    if search_name:
        author_query &= Q(full_name__icontains=search_name)

    if search_email:
        author_query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(author_query).order_by('-full_name')

    if not authors:
        return ""

    output = []

    for a in authors:
        output.append(f'Author: {a.full_name}, email: {a.email}, status: {"Banned" if a.is_banned else "Not Banned"}')

    return '\n'.join(output)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if not top_author or top_author.num_articles == 0:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():
    reviewer = Author.objects.annotate(num_reviews=Count('author_reviews')).order_by('-num_reviews', 'email').first()

    if not reviewer or reviewer.num_reviews == 0:
        return ""

    return f"Top Reviewer: {reviewer.full_name} with {reviewer.num_reviews} published reviews."


def get_latest_article():

    last_article = Article.objects.order_by('-published_on').first()

    if last_article is None or last_article.title is None:
        return ""

    authors = last_article.authors.all().order_by('full_name')
    author_names = ", ".join([author.full_name for author in authors])

    reviews = last_article.article_reviews.all()

    num_reviews = reviews.count()
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

    if avg_rating is None:
        avg_rating = 0

    return f"The latest article is: {last_article.title}. Authors: {author_names}. Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():

    top_article = Article.objects.filter(article_reviews__isnull=False).annotate(avg_rating=Avg('article_reviews__rating')).order_by('-avg_rating', 'title').first()

    if not top_article:
        return ""

    num_reviews = top_article.article_reviews.count()
    avg_rating = top_article.avg_rating

    return f"The top-rated article is: {top_article.title}, with an average rating of {avg_rating:.2f}, reviewed {num_reviews} times."


def ban_author(email=None):

    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews = author.author_reviews.count()

    author.author_reviews.all().delete()

    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
