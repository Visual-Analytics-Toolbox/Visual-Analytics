from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse

urlpatterns = [
    path("", include("user.urls")),
    path('csrf/', ensure_csrf_cookie(lambda request: HttpResponse(status=204)), name='csrf'),
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("common.urls")),
    path("api/", include("cognition.urls")),
    path("api/", include("motion.urls")),
    path("api/", include("image.urls")),
    path("api/", include("behavior.urls")),
    path("api/", include("annotation.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = urlpatterns + debug_toolbar_urls()
