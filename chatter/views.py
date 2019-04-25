from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,TemplateView
from django.contrib.auth.views import LoginView
from chatter.models import Message,User,Chatter,Group,GroupMembership
from django.utils.timezone import now
# Create your views here.

class Index(TemplateView):
	template_name = 'index.html'
	def get_context_data(self, **kwargs):
		context = {}
		context['user'] = self.request.user
		return context
class GroupList(ListView):
	model = Group
	def get_queryset(self):
		print(Group.objects.filter(groupmembership__user=self.request.user))
		return Group.objects.filter(groupmembership__user=self.request.user)
class GroupDetail(DetailView):
	model = Group
	context_object_name = 'c'
	def get_more_context_data(self, **kwargs):
		kwargs.setdefault('view', self)
		group_object = self.get_object()
		kwargs.update({'group_members_list':group_object.members.all(),'messages':group_object.messages.all(),'user':self.request.user})
		return kwargs
	def get_context_data(self, **kwargs):
		context = {}
		if self.object:
			context['object'] = self.object
			context_object_name = self.get_context_object_name(self.object)
			if context_object_name:
				context[context_object_name] = self.object
		context.update(kwargs)
		context=self.get_more_context_data()
		return super().get_context_data(**context)
	def post(self,*args,**kwargs):
		try:
			new_message = Message()
			new_message.message_text = self.request.POST['message_text']
			new_message.sender = self.request.user
			new_message.group = self.get_object()
			new_message.sent_at = now()
			new_message.save()
		except:
			pass
		return self.get(*args,**kwargs)
class GroupCreate(CreateView):
	model = Group
	fields = ['name']
	success_url = reverse_lazy('groups')
	def post(self,*args,**kwargs):
		try:
			new_group = Group()
			new_group.name = self.request.POST['group_name']
			new_group.save()
			membership = GroupMembership()
			membership.user = self.request.user
			membership.group = new_group
			membership.role = '2'
			membership.save()
		except:
			pass
		return self.get(self,*args,**kwargs)
class ChatterLogin(LoginView):
	model = Chatter
	success_url = reverse_lazy('groups')
