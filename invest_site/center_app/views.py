from django.shortcuts import render


def index(request):
    return render(request, "center_app/chat/index.html")


def room(request, room_name):
    return render(request, "center_app/chat/chat_room.html", {"room_name": room_name})