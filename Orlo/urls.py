from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import include, path

from django.conf import settings;
from django.conf.urls.static import static

admin.site.site_header = "Orlo Administration"
admin.site.site_title = "Orlo Administration Portal"
admin.site.index_title = "Orlo Administration Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('', include('orders.urls')),
    path('', include('payments.urls')),
    path('', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
