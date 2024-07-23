from django.contrib import admin
from watchlist_app.models import Watchlist, StreamPlatform, Reviews

# Register your models here.

admin.site.register(Watchlist)
admin.site.register(StreamPlatform)
admin.site.register(Reviews)