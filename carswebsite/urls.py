from django.contrib import admin
from django.urls import path
from cars import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('signup/', views.signup_view, name='signup'),

    path('car/<int:id>/', views.car_detail, name='car_detail'),

    path('dealer-dashboard/', views.dealer_dashboard, name='dealer_dashboard'),

    # ✅ ADD THIS
    path('delete-car/<int:id>/', views.delete_car, name='delete_car'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('privacy/', views.privacy, name='privacy'),

    path('terms/', views.terms, name='terms'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)