from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('register',views.register_view,name="register" ),

    path('hotel-detail/<uid>/', views.hotel_detail, name='hotel_detail'),
    path('login',views.login_view,name="login" ),
    path('logout',views.logout_view,name="logout" ),
    path('',views.index,name="index" ),
    path('reservation',views.reservations,name="reservation" ),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()