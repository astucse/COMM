from django.contrib import admin
from .models import Group,GroupMembership,Message,Chatter
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Message)
admin.site.register(Chatter)
