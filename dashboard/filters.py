from django.contrib.auth.models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains', ],
            # 'first_name': ['icontains', ],
            # 'last_name': ['exact', ],
            # 'date_joined': ['year', 'year__gt', 'year__lt', ],
        }