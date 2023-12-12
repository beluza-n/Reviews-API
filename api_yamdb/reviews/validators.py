from django.utils import timezone
from django.core.exceptions import ValidationError


def title_year_validation(value):
    current_year = timezone.now().year
    if not isinstance(value, int):
        raise ValidationError('Год должен быть целым числом!')
    if value is None:
        raise ValidationError('Год должен быть заполнен!')
    if value > current_year:
        raise ValidationError('Год выпуска не может быть больше текущего!')