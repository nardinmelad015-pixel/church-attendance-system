from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("", views.landing, name="landing"),

    path("login/", auth_views.LoginView.as_view(), name="login"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
    "logout/",
    auth_views.LogoutView.as_view(
        next_page="/"
    ),
    name="logout"
),

path(
    "schedule/<int:schedule_id>/confirm/",
    views.confirm_schedule,
    name="confirm_schedule"
),
path(
    "servants/",
    views.servant_list,
    name="servant_list"
),

path(
    "servant/<int:servant_id>/",
    views.servant_detail,
    name="servant_detail"
),
path(
    "servant/<int:servant_id>/edit/",
    views.edit_servant,
    name="edit_servant"
),

path(
    "servant/<int:servant_id>/delete/",
    views.delete_servant,
    name="delete_servant"
),
path(
    "servant/<int:servant_id>/qr/",
    views.servant_qr,
    name="servant_qr"
),
path(
    "send-notifications/<int:meeting_id>/",
    views.send_notifications,
    name="send_notifications",
),
path(
    "excuse/<int:excuse_id>/approve/",
    views.approve_excuse,
    name="approve_excuse"
),
path(
    "excuse/<int:excuse_id>/reject/",
    views.reject_excuse,
    name="reject_excuse"
),
path(
    "schedule/<int:schedule_id>/excuse/",
    views.excuse_schedule,
    name="excuse_schedule"
),
path(
    "servants/add/",
    views.add_servant,
    name="add_servant"
),
path("meetings/", views.meeting_list, name="meeting_list"),
path("meetings/add/", views.add_meeting, name="add_meeting"),
path(
    "meeting/<int:meeting_id>/checkin/",
    views.meeting_checkin,
    name="meeting_checkin"
),
path(
    "meeting/<int:meeting_id>/qr/",
    views.meeting_qr,
    name="meeting_qr"
),
path(
    "schedule/add/",
    views.add_schedule,
    name="add_schedule"
),

path(
    "schedule/",
    views.schedule_list,
    name="schedule_list"
),
    path('excuse/list/', views.excuse_list, name='excuse_list'),
    path('excuse/add/', views.add_excuse, name='add_excuse'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
]