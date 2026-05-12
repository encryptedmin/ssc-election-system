from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('', include('dashboard.urls')),

    path('accounts/', include('accounts.urls')),

    path('elections/', include('elections.urls')),

    path('candidates/', include('candidates.urls')),

    path('results/', include('results.urls')),
    path('voters/', include('voters.urls')),
    path('voting/', include('voting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
elif getattr(settings, 'SERVE_MEDIA', False):
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
