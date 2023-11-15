from decimal import Decimal

from django.db import models
from django.db.models import Count, QuerySet, Max, Min, Avg


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        return self.values('location').annotate(visit_count=Count('location')).order_by('-visit_count', 'location')[:2]


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet:
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        max_rating = self.aggregate(max_rating=Max('rating'))['max_rating']
        return self.filter(rating=max_rating).first()

    def lowest_rated_game(self):
        min_rating = self.aggregate(min_rating=Min('rating'))['min_rating']
        return self.filter(rating=min_rating).first()

    def average_rating(self):
        average_rating = self.aggregate(avg_rating=Avg('rating'))

        return f"{average_rating['avg_rating']:.1f}"





