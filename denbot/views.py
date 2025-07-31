from django.shortcuts import render


def index(request):
    if request.user.is_anonymous:
        return render(request, 'denbot/public/index.html')
    else:
        return render(request, 'denbot/authed/index.html')