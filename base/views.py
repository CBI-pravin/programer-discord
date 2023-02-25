

from http.client import HTTPResponse

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Message, Room , Topic, User
from .forms import RoomForm,UserForm,UpdateUserForm, MyUserCreationForm


from django.db.models import Q

# here we are importing user model from django admin 

# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')

        try:
            user = User.objects.get(username = username1)
            
        except:
            messages.error(request,' user does not exist' )

        user = authenticate(request,username = username1,password = password1)
        
        if user is not None:
            login(request,user)
            return redirect('home')  
        else:
            messages.error(request,'user name or password are not valid')          
    context ={'page':page}
    return render(request, 'base/login_register.html',context)





def logoutPage(request):
    logout(request)
    
    return redirect('home')







def registerPage(request):
    
    

    # if request.method == 'POST':
    #     pass1=request.POST.get('password1')
    #     pass2=request.POST.get('password2')
    #     if pass1 == pass2:
    #         if User.objects.filter(email=email).exists():
    #             message = messages.error(request,'email alredy register')
    #             return render(request,'base/login_register.html')
    #         else:
    #             user = User.objects.create(username=username,name=name,email=email,password = pass1)
    #             user.set_password(pass1)
    #     else:
    #         messages.error(request,'something went wrong')

    # if form.is_valid():
    #     user = form.save(commit=False)
    #     user.username=user.username
    #     user.save()
    #     login(request,user)
    #     redirect('home')
    # else:
    #     messages.error(request,"error in saving info")`
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
                # commit is to directly use create user credientials
            user = form.save(commit=False)
                # user.username =user.username
            user.save()
            login(request,user)
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request,'{}'.format(form.errors))
    else:
        form = MyUserCreationForm()

    context ={'form': form}


    return render(request,'base/login_register.html',context)






def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|Q (name__icontains=q) |Q (description__icontains=q) )
    # this is home page topics limit to 8 topic at page
    topics = Topic.objects.all()[0:8]
    room_count= rooms.count()
    # this is fro rescent sctivity we casn put limit to no of message
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms,'topics':topics, 'room_count': room_count,'room_messages':room_messages}
    # rooms = Room.objects.all()
    return render(request,'base/home.html',context)








@login_required(login_url='login')
def room(request,pk):
    """this function is to send message through chat rooms"""
    room = Room.objects.get(id = pk)
    # - is for most rescent message
    room_messages =room.message_set.all()

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body')

        )
        room.participants.add(request.user)
        # room.participants.remove()

        # there is also remove method available
        return redirect('room',pk=room.id)


    context ={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)







def userProfile(request,pk):
    user =User.objects.get(id=pk)

    # to get users chat room we can get all children obj by specifying modelname_set.condition
    rooms= user.room_set.all()

    room_messages= user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html' ,context)








@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics=Topic.objects.all()

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        # 
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(

            host=request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(request.POST)

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host= request.user
        #     room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html',context)







@login_required(login_url='login')
def updateRoom(request, pk):
    room =Room.objects.get(id=pk)
    # this form will be prefilled by instance
    form = RoomForm(instance=room)  
    topics=Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you are not alooed ')

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
            # instance is to say that not create a new form insted update the provided instance form
        # form= RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
        return redirect('home')

    context ={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method== 'POST':
        room.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':room})




@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method== 'POST':
        message.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':message})




@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'account update succesfully')
            redirect('user-profile',pk=user.id)
    context ={'form':form}
    return render(request,'base/update-user.html',context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    topics=Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)


def activityPage(request):
    room_messages= Message.objects.all()
    context ={'room_messages':room_messages}
    return render(request,'base/activity.html',context)