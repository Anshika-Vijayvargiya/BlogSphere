from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Blog,Favourite
from .forms import addform,editform
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth
from rest_framework import viewsets,status
from rest_framework.response import Response
from blog.serializer import BlogSerializer
from django.core.paginator import Paginator

# Create your views here.
def openp(request):
    return render(request,"openp.html")


def home(request):
    blog=Blog.objects.filter(status="Published")
    fav_blog=Favourite.objects.filter(user=request.user).values_list("blog_id",flat=True)
    paginator=Paginator(blog,4)
    page_number = request.GET.get('page')  # Get the page number from the query params
    obj = paginator.get_page(page_number)
    return render(request,"index.html",{"obj":obj,"fav_blog":fav_blog})

def addBlog(request):
    if request.method=="POST":
        f=addform(request.POST)
        if f.is_valid():
            p=f.save(commit=False)
            p.author=request.user
            f.save()
            return redirect("blog:home")
        
    else:
        f=addform()
    return render(request,"add.html",{"f":f})

def publish(request,id):
    i=get_object_or_404(Blog,id=id)
    i.status="Published"
    i.save()
    return redirect("blog:home")




def editblog(request,id):
    i=get_object_or_404(Blog,id=id)
    if request.method=="POST":
       f=editform(request.POST,instance=i)
       if f.is_valid():

        p=f.save()
        return redirect("blog:home")
       return HttpResponse("hello")
    
    else:
        f=editform(instance=i)
    return render(request,"edit.html",{"i":i})

def draft(request):
    obj=Blog.objects.filter(status="Draft",author=request.user)
    return render(request,"drafts.html",{"obj":obj})

def delete_post(request,id):
    i=get_object_or_404(Blog,pk=id)
    
    
    i.delete()
    return redirect("blog:home")
        
    # return render(request,"index.html",{"i":i})
def remFav(request,id):
    i=get_object_or_404(Favourite,pk=id)
    
    
    i.delete()
    return redirect("blog:favourite")

def addFav(request,id):
    blog=get_object_or_404(Blog,id=id)
    if not Favourite.objects.filter(user=request.user,blog=blog).exists():
        Favourite.objects.create(user=request.user,blog=blog)
        return redirect("blog:favourite")
    return redirect("blog:home")

def favourite(request):
    obj=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"obj":obj})

def register(request):
   if request.method=="POST":
       username=request.POST["username"]
       email=request.POST["email"]
       password=request.POST["password"]
       cpassword=request.POST["cpassword"]

       if cpassword==password:
           if User.objects.filter(email=email).exists():
               messages.info(request,"email already exists")
               return redirect("blog:register")
                
           elif User.objects.filter(email=email).exists():
               messages.info(request,"USername already exists")
               return redirect("blog:register")
           
           else:
               user=User.objects.create_user(username=username,email=email,password=password)
               user.save()
               return redirect("blog:login")
                
       else:
           messages.info(request,"password doesnot match")
           return redirect("blog:register")
   else:
       return render(request,"register.html")
   
def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        if not User.objects.filter(username=username).exists():
            messages.info(request,"Invalid Username")
            return redirect("blog:login")
        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request,"Invalid Password")
            return redirect("blog:login")
        else:
            auth.login(request,user)
            return redirect("blog:home")
    
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect("/")

    
    
#api viewset

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class=BlogSerializer
    queryset=Blog.objects.all()

    def create(self,request,*args,**kwargs):
        data=request.data
        serializer=self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Blog has been created","data": serializer.data},status=status.HTTP_201_CREATED)
    
    def update(self,request,*args,**kwargs):
        partial=kwargs.pop("partial",False)
        instance=self.get_object()
        data=request.data
        serializer=self.get_serializer(instance,data=data,partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Blog has been Updated","data": serializer.data},status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        return Response({"message":f"Blog {instance.title} has been deleted"})
        

    

