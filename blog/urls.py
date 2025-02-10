from django.urls import path,include
from . import views
from rest_framework import routers
from blog.views import BlogViewSet

app_name='blog'

router=routers.SimpleRouter()
router.register("blog",BlogViewSet)

urlpatterns = [path("home",views.home,name="home"),
               path("",views.openp,name="openp"),
               path("add/",views.addBlog,name="add"),
               path("delete/<id>/",views.delete_post,name="delete"),
               path("publish/<id>/",views.publish,name="publish"),
               path("register",views.register,name="register"),
               path("login",views.login,name="login"),
               path("logout",views.logout,name="logout"),
               path("edit/<id>",views.editblog,name="edit"),
               path("draft",views.draft,name="draft"),
               path("addFav/<id>/",views.addFav,name="addFav"),
               path("remFav/<id>/",views.remFav,name="remFav"),
               path("favourite",views.favourite,name="favourite"),
               path("api/",include(router.urls))
               ]


