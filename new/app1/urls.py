from django.urls import path
from . import views



urlpatterns = [

    path("signup/", views.sign_up, name="signup"),
    path("login/",views.login,name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("logout",views.logout,name="logout"),


#api

path("api/get",views.student_list),
path("api/get/<int:id>",views.student_detail),
path("api/create",views.student_add),
path("api/update/<int:id>",views.student_update),
path("api/pupdate/<int:id>",views.student_partial_update),
path("api/delete/<int:id>",views.student_delete),
  

]