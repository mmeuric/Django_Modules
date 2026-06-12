from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello World !")


if __name__ == '__main__':
    hello_world(None)
