from django.core.exceptions import ValidationError
from django.db import models
from datetime import date, timedelta


class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        age = today - self.birth_date
        return age // timedelta(days=365.25)


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    class AnimalChoices(models.TextChoices):
        MAMMALS = 'Mammals'
        BIRDS = 'Birds'
        REPTILES = 'Reptiles'
        OTHERS = 'Others'

    specialty = models.CharField(max_length=10, choices=AnimalChoices.choices)
    managed_animals = models.ManyToManyField(to=Animal)

    def clean(self):
        if self.specialty not in self.AnimalChoices.values:
            raise ValidationError('Specialty must be a valid choice.')


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [(True, 'Available'), (False, 'Not Available')]
        kwargs['default'] = True
        super(BooleanChoiceField, self).__init__(*args, **kwargs)


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

    def is_available(self):
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        info = f"Meet {self.name}! It's {self.species} and it's born {self.birth_date}. It makes a noise like '{self.sound}'!"

        if hasattr(self, 'mammal'):
            info += f" Its fur color is {self.mammal.fur_color}."
        elif hasattr(self, 'bird'):
            info += f" Its wingspan is {self.bird.wing_span} cm."
        elif hasattr(self, 'reptile'):
            info += f" Its scale type is {self.reptile.scale_type}."

        return info

    def is_endangered(self):
        endangered_species = ["Cross River Gorilla", "Orangutan", "Green Turtle"]
        return self.species in endangered_species
