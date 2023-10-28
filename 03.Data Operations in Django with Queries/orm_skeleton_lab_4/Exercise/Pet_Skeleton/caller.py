import os

import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


def create_pet(name: str, species: str):
    pets = Pet.objects.all().create(
        name=name,
        species=species
    )

    return f"{pets.name} is a very cute {pets.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.all().create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


def create_location(name, region, population, description, is_capital):
    Location.objects.all().create(
        name=name,
        region=region,
        population=population,
        description=description,
        is_capital=is_capital
    )


def show_all_locations():
    location = Location.objects.order_by('-id')

    return '\n'.join(str(l) for l in location)


def new_capital():
    make_capital = Location.objects.first()

    if make_capital:
        make_capital.is_capital = True
        make_capital.save()


def get_capitals():
    show_capital = Location.objects.filter(is_capital=True).values('name')

    return show_capital


def delete_first_location():
    Location.objects.first().delete()


def create_car(model, year, color, price):
    Car.objects.all().create(
        model=model,
        year=year,
        color=color,
        price=price,

    )


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        year = car.year
        price = car.price

        percentage_off = sum(int(x) for x in str(year)) / 100
        discount = float(car.price) * percentage_off
        car.price_with_discount = float(price) - discount
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.filter(year__gte=2020)
    recent_cars = recent_cars.values('model', 'price_with_discount')
    return recent_cars


def delete_last_car():
    Car.objects.last().delete()


def create_task(title, description, due_date):
    Task.objects.all().create(
        title=title,
        description=description,
        due_date=due_date,
    )


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(str(t) for t in unfinished_tasks)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    tasks = Task.objects.filter(title=task_title)
    new_text = "".join(chr(ord(l) - 3) for l in text)

    for task in tasks:
        task.description = new_text
        task.save()


def create_hotel_rooms(room_number, room_type, capacity, amenities, price_per_night):
    HotelRoom.objects.all().create(
        room_number=room_number,
        room_type=room_type,
        capacity=capacity,
        amenities=amenities,
        price_per_night=price_per_night
    )


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    info_for_the_room = []

    for r in deluxe_rooms:
        if r.id % 2 == 0:
            info_for_the_room.append(f'Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!')

    return '\n'.join(info_for_the_room)


def increase_room_capacity():
    previous_capacity = None
    all_rooms = HotelRoom.objects.order_by('id')

    for room in all_rooms:
        if not room.is_reserved:
            continue

        if previous_capacity:
            room.capacity += previous_capacity
        else:
            room.capacity += room.id
        previous_capacity = room.capacity
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()

    if first_room:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved:
        last_room.delete()

