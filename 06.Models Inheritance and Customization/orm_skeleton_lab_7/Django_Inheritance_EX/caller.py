import os
from datetime import date

import django
from django.core.exceptions import ValidationError

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Necromancer, Mage, UserProfile, Message, Student, CreditCard, Hotel, Room, \
    SpecialReservation

# mage = Mage.objects.create(
#     name="Fire Mage",
#     description="A powerful mage specializing in fire magic.",
#     elemental_power="Fire",
#     spellbook_type="Ancient Grimoire"
# )
#
# necromancer = Necromancer.objects.create(
#     name="Dark Necromancer",
#     description="A mage specializing in dark necromancy.",
#     elemental_power="Darkness", spellbook_type="Necronomicon",
#     raise_dead_ability="Raise Undead Army"
# )
#
# print(mage.elemental_power)
# print(mage.spellbook_type)
# print(necromancer.name)
# print(necromancer.description)
# print(necromancer.raise_dead_ability)

# user1 = UserProfile.objects.create(username='john_doe', email='john@example.com', bio='Hello, I am John Doe.')
# user2 = UserProfile.objects.create(username='jane_smith', email='jane@example.com', bio='Hi there, I am Jane Smith.')
# user3 = UserProfile.objects.create(username='alice', email='alice@example.com', bio='Hello, I am Alice.')
#
# message1 = Message.objects.create(
#     sender=user1,
#     receiver=user2,
#     content="Hello, Jane! Could you please tell Alice that tomorrow we are going on vacation?")
# print(message1.content)
#
# message1.mark_as_read()
# print(f"Is read: {message1.is_read}")
#
# reply_message = message1.reply_to_message(
#     receiver=user1,
#     reply_content="Hi John, sure! I will forward this message to her!")
# print(reply_message.content)
#
# forwarded_message = message1.forward_message(sender=user2, receiver=user3)
# print(f"Forwarded message from {forwarded_message.sender.username} to {forwarded_message.receiver.username}")

# student1 = Student(name="John", student_id=12345)
# student1.save()
#
# student2 = Student(name="Alice", student_id=45.23)
# student2.save()
#
# student3 = Student(name="Bob", student_id="789")
# student3.save()
#
# retrieved_student1 = Student.objects.get(name="John")
# retrieved_student2 = Student.objects.get(name="Alice")
# retrieved_student3 = Student.objects.get(name="Bob")
#
# print(retrieved_student1.student_id)
# print(retrieved_student2.student_id)
# print(retrieved_student3.student_id)

# credit_card1 = CreditCard.objects.create(card_owner="Krasimir", card_number="1234567890123450")
# credit_card2 = CreditCard.objects.create(card_owner="Pesho", card_number="9876543210987654")
# credit_card3 = CreditCard.objects.create(card_owner="Vankata", card_number="4567890123456789")
#
# credit_card1.save()
# credit_card2.save()
# credit_card3.save()
#
# credit_cards = CreditCard.objects.all()
#
# for credit_card in credit_cards:
#     print(f"Card Owner: {credit_card.card_owner}")
#     print(f"Card Number: {credit_card.card_number}")

# hotel = Hotel.objects.create(name="Hotel ABC", address="123 Main St")
# room1 = Room.objects.create(hotel=hotel, number="101", capacity=2, total_guests=1, price_per_night=100.00)
# special_reservation1 = SpecialReservation(
#     room=room1,
#     start_date=date(2023, 1, 1),
#     end_date=date(2023, 1, 5)
# )
#
# print(special_reservation1.save())
#
# special_reservation2 = SpecialReservation(
#     room=room1,
#     start_date=date(2023, 1, 10),
#     end_date=date(2023, 1, 12)
# )
#
# print(special_reservation2.save())
#
# print(special_reservation1.calculate_total_cost())
# print(special_reservation1.reservation_period())
#
# try:
#     special_reservation1.extend_reservation(5)
# except ValidationError as e:
#     print(e)