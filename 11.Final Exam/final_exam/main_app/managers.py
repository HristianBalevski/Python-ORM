from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):

    def get_authors_by_article_count(self):

        return self.annotate(num_articles=Count('articles')).order_by('-num_articles', 'email')