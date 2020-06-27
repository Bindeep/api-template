import re

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core.utils.helpers import get_today, combine_date_parts

PHONE_NUMBER_REGEX = re.compile(r"^(([+]?\d{3})-?)?\d{7,10}$")


def validate_name(name):
    if not name.replace(" ", "").isalpha():
        raise serializers.ValidationError(
            _("Name Should not contain any special characters."))
    return name


def validate_phone_number_without_country_code(number):
    phone_number = str(number)
    if not 7 <= len(phone_number) <= 10:
        raise serializers.ValidationError(
            _('Phone Number should range from 7-10.')
        )

    if not phone_number.isdigit():
        raise serializers.ValidationError(
            _('Phone Number Should Be Integer')
        )


def validate_phone_number(number):
    phone_number = str(number)

    if not PHONE_NUMBER_REGEX.match(phone_number):
        raise serializers.ValidationError(
            _('Phone Number format is not valid. Some examples of supported'
              ' phone numbers are numbers are 9811111111, 08256666,'
              ' 977-9833333333, +977-9833333333, 977-08256666')
        )

    return number


def validate_coded_phone_number(number):
    number = str(number)
    try:
        country_code, phone_number = number.split('-')
    except ValueError:
        raise serializers.ValidationError(
            _('Phone Number format is incorrect.')
        )

    validate_phone_number_without_country_code(phone_number)

    if not country_code.isdigit():
        raise serializers.ValidationError(
            _('Country Code Should Be Integer')
        )

    # TODO: add more validation rule
    return number


def validate_otp(otp):
    """
    Validate Otp
    :param otp:
    :return:
    """
    otp = str(otp)

    if not len(otp) == settings.OTP_LENGTH:
        raise serializers.ValidationError(
            _(f'Otp should have length of {settings.OTP_LENGTH}')
        )
    return otp


def validate_dob(value):
    year_diff = get_today().year - value.year
    if year_diff not in range(16, 100):
        raise serializers.ValidationError(
            _('Age must be in between 16 years and 100 years.'))
    return value


def is_future_datetime(value, error_message=_("DateTime Must Be Future.")):
    if not timezone.now() < value:
        raise serializers.ValidationError(error_message)
    return value


def validate_attachment(attachment):
    if attachment.size > settings.ATTACHMENT_MAX_UPLOAD_SIZE:
        raise serializers.ValidationError(
            _(
                'File Size Should not Exceed '
                f'{settings.ATTACHMENT_MAX_UPLOAD_SIZE / (1024 * 1024)} MB'
            )
        )
    return attachment


def validate_future_datetime(year: int = 0, month: int = 0, day: int = 1):
    """
    compares provided_date with today's date and raises validation error
    if provided_date is greater than today's date

    """

    provided_date = combine_date_parts(year, month, day)

    if not provided_date:
        raise serializers.ValidationError(_(
            'Invalid Date Passed.'
        ))

    if provided_date > get_today():
        raise serializers.ValidationError(_(
            'Date Must not be in future.'
        ))


def validate_is_future_datetime(year: int = 0, month: int = 0, day: int = 1):
    """
    compares provided_date with today's date and raises validation error
    if provided_date is less than today's date
    """

    provided_date = combine_date_parts(year, month, day)

    if not provided_date:
        raise serializers.ValidationError(_(
            'Invalid Date Passed.'
        ))

    if provided_date < get_today():
        raise serializers.ValidationError(_(
            'Date Must be in future.'
        ))
