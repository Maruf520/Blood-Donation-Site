from django.core.exceptions import ValidationError


def valid_group(group, bank):
    print(bank, group)
    if group and bank.blood_set.filter(group=group).exists():
        return ValidationError('Try to add different group')
