from django.contrib import admin
from django.urls import path, include
from simple_admin import views
from django.conf import settings

urlpatterns = [
    path("", views.index, name='index'),
    path("admin/login/", views.user_login),
    path("admin/", admin.site.urls),
    path("send_email/", views.SendUsersEmails.as_view(), name="send_email"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.logout, name="logout"),
    path("broadcast/", views.broadcast_mail, name="broadcast_mail"),
    path("custom_admin/", views.custom_admin, name="custom_admin"),
    path("unauthorized/", views.unauthorized, name="unauthorized"),
    path("activate/<int:user_id>", views.toggle_user_status_true, name="toggle_user_status_true"),
    path("deactivate/<int:user_id>", views.toggle_user_status_false, name="toggle_user_status_false"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns