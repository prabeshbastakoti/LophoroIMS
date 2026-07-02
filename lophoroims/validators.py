from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[0-9\- ]{7,15}$",
    message="Enter a valid phone number (digits, spaces, hyphens, and an optional leading + only).",
)

pan_validator = RegexValidator(
    regex=r"^\d{9}$",
    message="PAN number must be exactly 9 digits.",
)
