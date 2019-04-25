from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Chatter(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username
class Group(models.Model):
	name = models.CharField(max_length=200)
	is_private = models.BooleanField(default=False)
	members = models.ManyToManyField(User, through='GroupMembership', related_name='member_groups')

class GroupMembership(models.Model):
	ROLE_CHOICE = (('1', 'Admin'),
				   ('2', 'Member'),)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	role = models.CharField(choices=ROLE_CHOICE, default='2', max_length=1,null=True,blank=True)

class Message(models.Model):
	message_text = models.TextField(max_length=255)
	sender = models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
	recipient = models.ForeignKey(User,related_name='recieved_messages',on_delete=models.CASCADE,null=True,blank=True)
	group = models.ForeignKey(Group,related_name='messages',on_delete=models.CASCADE,null=True)
	# reply_to = models.ForeignKey(Message,null=True,blank=True,on_delete=models.CASCADE) #TODO make this work
	sent_at = models.DateTimeField(null=True,blank=True)
	read_at = models.DateTimeField(null=True,blank=True)
	deleted_at = models.DateTimeField(null=True,blank=True)

def inbox_count_for(user):
	return Message.objects.filter(recipient=user, read_at__isnull=True, deleted_at__isnull=True).count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Chatter.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.chatter.save()

