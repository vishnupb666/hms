from django.contrib import admin
from .models import role,department,user_ext,doctor,appointment,leave
# Register your models here.
admin.site.register(user_ext)
admin.site.register(role)
admin.site.register(department)
admin.site.register(doctor)
admin.site.register(appointment)
admin.site.register(leave)