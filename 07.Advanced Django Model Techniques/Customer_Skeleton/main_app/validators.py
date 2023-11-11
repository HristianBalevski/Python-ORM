from django.core.exceptions import ValidationError


def validate_name(value):
    for symbol in value:
        if not symbol.isalpha() and not symbol.isspace():
            raise ValidationError("Name can only contain letters and spaces")


def validate_phone_number(value):
    if not value.startswith('+359') or not value[4:].isdigit() or len(value) != 13:
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")


