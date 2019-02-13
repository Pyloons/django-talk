from django.conf.urls import url
from .views import IndexView, LoginView, RegistView, UserView, LogoutView


urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r"^register/$", RegistView.as_view(), name="register"),
    url(r"^user/$", UserView.as_view(), name="user"),
]