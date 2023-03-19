from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('myprofile/', views.profile_view, name='myprofile'),
    path('my-invites/', views.invites_received_view, name='my-invites-view'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('all-invites/', views.invite_profile_list_view, name='all-invites-view'),
    path('send-invite/', views.send_invatation, name='send-invite'),
    path('remove-friend/', views.remove_friend, name='remove-friend'),
    path('my-invites/accept/', views.accept_request, name="accept-invite"),
    path('my-invites/reject/', views.reject_request, name="reject-invite"),
]