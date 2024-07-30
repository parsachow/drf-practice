
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/', include('watchlist_app.api.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('account/', include('user_app.api.urls')),
]
