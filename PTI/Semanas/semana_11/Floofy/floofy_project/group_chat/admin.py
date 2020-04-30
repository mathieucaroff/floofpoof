from django.contrib import admin

# Register your models here.
from .models import Thread, Message

class Message(admin.TabularInline):
    model = Message

class ThreadAdmin(admin.ModelAdmin):
    inlines = [Message]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)