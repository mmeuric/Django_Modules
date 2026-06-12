from django.urls import path
from . import views


def get_urlpatterns():
    return [
        path('', views.hello_world, name='hello_world'),
    ]


urlpatterns = get_urlpatterns()


if __name__ == '__main__':
    get_urlpatterns()
