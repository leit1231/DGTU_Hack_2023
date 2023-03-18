from django.shortcuts import render
from forms import *
from .models import *
from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import ChatSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        message = serializer.validated_data['message']
        room_name = self.kwargs['room_name']

        # Send message to room group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


def create_post(request):
    if request.method == 'POST':
        form = AddcourseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('home')
    else:
        form = AddcourseForm()
    return render(request, 'create_post.html', {'form': form})
