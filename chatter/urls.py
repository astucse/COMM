from django.urls import path
from . import views

urlpatterns = [
	path('',views.Index.as_view()),
	path('groups/',views.GroupList.as_view(),name='groups'),
	path('groups/<int:pk>',views.GroupDetail.as_view(),name='group_detail'),
	path('groups/create/',views.GroupCreate.as_view(),name='group_create'),
	path('groups/<int:pk>/adduser/',views.GroupAddUser.as_view(),name='group_add_user'),
	path('login/',views.ChatterLogin.as_view(),name='login')
]
  