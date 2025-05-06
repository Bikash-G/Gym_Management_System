from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.handle_login, name='handle_login'),
    path('logout', views.logout_user, name='logout_user'),
    path('contact', views.contact, name='contact'),
    path('enroll', views.enroll, name='enroll'),
    path('explore_plans', views.explore_plans, name='explore_plan'),
    path('profile', views.profile, name='profile'),
    path('about', views.about, name='about'),
    path("feedback",views.feedback,name="feedback"),


#   admin urls
    path("admin_home",views.dashboard,name="dashboard"),

    # admin contact urls
    path("delete_contact/<id>",views.delete_contact,name="delete_contact"),

#    admin member urls
    path("add_member",views.add_member,name="add_member"),
    path("edit_member/<id>",views.edit_member,name="edit_member"),
    path("delete_member/<id>",views.delete_member,name="delete_member"),

#   admin membership plan urls 
    path("add_membership",views.add_membership,name="add_membership"),
    path("edit_membership/<id>",views.edit_membership,name="edit_membership"),
    path("delete_membership/<id>",views.delete_membership,name="delete_membership"),

#   admin trainer urls 
    path("add_trainer",views.add_trainer,name="add_trainer"),
    path("edit_trainer/<id>",views.edit_trainer,name="edit_trainer"),
    path("delete_trainer/<id>",views.delete_trainer,name="delete_trainer"),

    #  delete feedback urls 
    path("delete_feedback/<id>",views.delete_feedback,name="delete_feedback"),

    
 
]