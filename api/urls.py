from django.urls import path
from .views import ItemList, ItemDetail, LocationList, LocationDetail, UserApiView, UserCurrent, AddArtist

urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<int:pk>/', ItemDetail.as_view()),
    path('location/', LocationList.as_view()),
    path('location/<int:pk>/', LocationDetail.as_view()),
    path('user/', UserApiView.as_view()),
    path('user/me', UserCurrent.as_view()),
    path('user/add-artist/', AddArtist.as_view()),
    path('user/<str:pk>/', UserApiView.as_view())
]
