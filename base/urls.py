from django.urls import path
from . import views

# str - Matches any non-empty string, excluding the path separator, '/'. 
#       This is the default if a converter isn’t included in the expression.
# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, 
#        plus the hyphen and underscore characters. For example, 
#        building-your-1st-django-site.
# uuid - Matches a formatted UUID. To prevent multiple URLs from mapping to 
#        the same page, dashes must be included and letters must be lowercase. 
#        For example, 075194d3-6885-417e-a8a8-6c931e272f00. Returns a UUID instance.
# path - Matches any non-empty string, including the path separator, '/'. 
#        This allows you to match against a complete URL path rather than a segment 
#        of a URL path as with str.

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]