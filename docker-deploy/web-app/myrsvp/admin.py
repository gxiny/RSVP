from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(RSVP)
admin.site.register(PlusOne)