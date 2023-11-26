from django.core.validators import MinLengthValidator
from django.db import models


class BaseClassMixin(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    published_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
