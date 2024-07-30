from django.urls import path
from .views_user import UserApiView, UserCurrent, AddArtist, RemoveArtist, AddFriend, RemoveFriend, UserFriends

urlpatterns = [
    path('user/', UserApiView.as_view()),
    path('user/me/', UserCurrent.as_view()),
    path('user/friends/', UserFriends.as_view()),
    path('user/add-artist/', AddArtist.as_view()),
    path('user/remove-artist/', RemoveArtist.as_view()),
    path('user/add-friend/', AddFriend.as_view()),
    path('user/remove-friend/', RemoveFriend.as_view()),
    path('user/<str:pk>/', UserApiView.as_view())

]
