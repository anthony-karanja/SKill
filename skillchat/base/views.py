# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib import messages
# from rest_framework.response import Response
# from .serializers import UserSerializer, TopicSerializer, RoomSerializer, MessageSerializer
# from django.contrib.auth.decorators import login_required
# from rest_framework import generics, status
# from django.db.models import Q
# from django.contrib.auth import authenticate, login, logout
# from .models import Room, Topic, Message, User
# from .forms import RoomForm, UserForm, MyUserCreationForm

# # Create your views here.


# class SkillLogin(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
#     def loginPage(request):
#         page = 'login'
#         if request.user.is_authenticated:
#             return redirect('home')

#         if request.method == 'POST':
#             email = request.POST.get('email').lower()
#             password = request.POST.get('password')

#             try:
#                 user = User.objects.get(email=email)
#             except:
#                 messages.error(request, 'User does not exist')

#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Username OR password does not exit')

#         # return Response(status=status.HTTP_200_OK)

#     def logoutUser(request):
#         logout(request)
#         return redirect('home')


#     def registerPage(request):
#         form = MyUserCreationForm()

#         if request.method == 'POST':
#             form = MyUserCreationForm(request.POST)
#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.username = user.username.lower()
#                 user.save()
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, 'An error occurred during registration')

#         return Response(serializer.data, status=status.HTTP_200_OK)

# class HomeTopic(generics.ListAPIView):
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer

#     def get(self, request, *args, **kwargs):
#         q = request.GET.get('q') if request.GET.get('q') != None else ''

#         rooms = Room.objects.filter(
#             Q(topic__name__icontains=q) |
#             Q(name__icontains=q) |
#             Q(description__icontains=q)
#         )

#         topics = Topic.objects.all()[0:5]
#         room_count = rooms.count()
#         room_messages = Message.objects.filter(
#             Q(room__topic__name__icontains=q))[0:3]

#         context = {'rooms': rooms, 'topics': topics,
#                 'room_count': room_count, 'room_messages': room_messages}
#         return Response(context,  status=status.HTTP_200_OK)
    

# class HomeRoom(generics.CreateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

#     def get(sekf, request, pk, *args, **kwargs):
#         room = Room.objects.get(id=pk)
#         room_messages = room.message_set.all()
#         participants = room.participants.all()

#         if request.method == 'POST':
#             message = Message.objects.create(
#                 user=request.user,
#                 room=room,
#                 body=request.POST.get('body')
#             )
#             room.participants.add(request.user)
#             return redirect('room', pk=room.id)

#         context = {'room': room, 'room_messages': room_messages,
#                 'participants': participants}
#         return Response(context,  status=status.HTTP_200_OK)


#     def userProfile(request, pk):
#         user = User.objects.get(id=pk)
#         rooms = user.room_set.all()
#         room_messages = user.message_set.all()
#         topics = Topic.objects.all()
#         context = {'user': user, 'rooms': rooms,
#                 'room_messages': room_messages, 'topics': topics}
#         return Response(context,  status=status.HTTP_200_OK)



#     @login_required(login_url='login')
#     def createRoom(request):
#         form = RoomForm()
#         topics = Topic.objects.all()
#         if request.method == 'POST':
#             topic_name = request.POST.get('topic')
#             topic, created = Topic.objects.get_or_create(name=topic_name)

#             Room.objects.create(
#                 host=request.user,
#                 topic=topic,
#                 name=request.POST.get('name'),
#                 description=request.POST.get('description'),
#             )
#             return redirect('home')

#         context = {'form': form, 'topics': topics}
#         return Response(context,  status=status.HTTP_200_OK)


# class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     lookup_field = 'pk'

#     @login_required(login_url='login')
#     def updateRoom(request, pk):
#         room = Room.objects.get(id=pk)
#         form = RoomForm(instance=room)
#         topics = Topic.objects.all()
#         if request.user != room.host:
#             return HttpResponse('Your are not allowed here!!')

#         if request.method == 'POST':
#             topic_name = request.POST.get('topic')
#             topic, created = Topic.objects.get_or_create(name=topic_name)
#             room.name = request.POST.get('name')
#             room.topic = topic
#             room.description = request.POST.get('description')
#             room.save()
#             return redirect('home')

#         context = {'form': form, 'topics': topics, 'room': room}
#         return Response(context,  status=status.HTTP_200_OK)


#     @login_required(login_url='login')
#     def deleteRoom(request, pk):
#         room = Room.objects.get(id=pk)

#         if request.user != room.host:
#             return HttpResponse('Your are not allowed here!!')

#         if request.method == 'POST':
#             room.delete()
#             return redirect('home')
#         return Response(status=status.HTTP_204_NO_CONTENT)


#     @login_required(login_url='login')
#     def deleteMessage(request, pk):
#         message = Message.objects.get(id=pk)

#         if request.user != message.user:
#             return HttpResponse('Your are not allowed here!!')

#         if request.method == 'POST':
#             message.delete()
#             return redirect('home')
#         return Response(status=status.HTTP_204_NO_CONTENT)


#     @login_required(login_url='login')
#     def updateUser(request):
#         user = request.user
#         form = UserForm(instance=user)

#         if request.method == 'POST':
#             form = UserForm(request.POST, request.FILES, instance=user)
#             if form.is_valid():
#                 form.save()
#                 return redirect('user-profile', pk=user.id)

#         return Response(status=status.HTTP_200_OK)


#     def topicsPage(request):
#         q = request.GET.get('q') if request.GET.get('q') != None else ''
#         topics = Topic.objects.filter(name__icontains=q)
#         # return render(request, 'base/topics.html', {'topics': topics})


#     def activityPage(request):
#         room_messages = Message.objects.all()
#         # return render(request, 'base/activity.html', {'room_messages': room_messages})
#         return Response(serializer.data, status=status.HTTP_200_OK)





from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TopicSerializer, RoomSerializer, MessageSerializer
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Class-based views for API endpoints
class SkillLogin(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def loginPage(request):
    if request.user.is_authenticated:
        return Response({'detail': 'User already authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        email = request.data.get('email').lower()
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def registerPage(request):
    form = MyUserCreationForm(request.data)

    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class HomeTopic(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q') if request.GET.get('q') else ''
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        topics = Topic.objects.all()[0:5]
        room_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]

        data = {
            'rooms': RoomSerializer(rooms, many=True).data,
            'topics': TopicSerializer(topics, many=True).data,
            'room_count': room_count,
            'room_messages': MessageSerializer(room_messages, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

class HomeRoom(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, pk, *args, **kwargs):
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()

        data = {
            'room': RoomSerializer(room).data,
            'room_messages': MessageSerializer(room_messages, many=True).data,
            'participants': UserSerializer(participants, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'pk'

@api_view(['POST'])
@login_required(login_url='login')
@permission_classes([IsAuthenticated])
def createRoom(request):
    form = RoomForm(request.data)
    if form.is_valid():
        room = form.save(commit=False)
        room.host = request.user
        room.save()
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@login_required(login_url='login')
@permission_classes([IsAuthenticated])
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

    form = RoomForm(request.data, instance=room)
    if form.is_valid():
        room = form.save()
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required(login_url='login')
@permission_classes([IsAuthenticated])
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

    room.delete()
    return Response({'detail': 'Room deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@login_required(login_url='login')
@permission_classes([IsAuthenticated])
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

    message.delete()
    return Response({'detail': 'Message deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@login_required(login_url='login')
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    form = UserForm(request.data, instance=user)

    if form.is_valid():
        user = form.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    return Response(TopicSerializer(topics, many=True).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def activityPage(request):
    room_messages = Message.objects.all()
    return Response(MessageSerializer(room_messages, many=True).data, status=status.HTTP_200_OK)
