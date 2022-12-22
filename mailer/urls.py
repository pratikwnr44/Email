from django.urls import path
from .views import activate, logoutView, sendMail, signup, loginView

urlpatterns = [
    path('send/', sendMail, name='sendmail_url'),
    path('su/', signup, name='signup_url'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('li/', loginView, name='login_url'),
    path('lo/', logoutView, name='logout_url'),
]