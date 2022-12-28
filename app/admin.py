from django.contrib import admin
from .models import Person,Count

# Register your models here.
admin.site.register(Person)
admin.site.register(Count)