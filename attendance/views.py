from django.shortcuts import render, redirect
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from .models import Servant, Attendance, Meeting, Excuse, Schedule
from .forms import AttendanceForm, ExcuseForm, ScheduleForm, ServantForm,MeetingForm
import qrcode
from .forms import CheckInForm
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Schedule
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def landing(request):
    return render(
        request,
        "attendance/landing.html"
    )


def approve_excuse(request, excuse_id):

    excuse = get_object_or_404(
        Excuse,
        id=excuse_id
    )

    excuse.status = "approved"
    excuse.save()

    return redirect("dashboard")

@login_required

def reject_excuse(request, excuse_id):

    excuse = get_object_or_404(
        Excuse,
        id=excuse_id
    )

    excuse.status = "rejected"
    excuse.save()

    return redirect("dashboard")


def send_notifications(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
        
        
    )
    

    schedules = Schedule.objects.filter(meeting=meeting)

    print("=" * 50)
    print("Meeting:", meeting)
    print("Schedules Found:", schedules.count())
    print("=" * 50)

    sent_count = 0

    for schedule in schedules:

        print("-" * 50)
        print("Servant:", schedule.servant.name)
        print("Email:", schedule.servant.email)
        print("Task:", schedule.task)
        print("-" * 50)

        if not schedule.servant.email:
            print("No email found")
            continue

        confirm_link = (
            f"http://192.168.100.6:8000"
            f"/schedule/{schedule.id}/confirm/"
        )

        excuse_link = (
            f"http://192.168.100.6:8000"
            f"/schedule/{schedule.id}/excuse/"
        )

        message = f"""
مرحباً {schedule.servant.name}

لديك خدمة قادمة

الاجتماع:
{schedule.meeting}

المهمة:
{schedule.task}

تأكيد الحضور:
{confirm_link}

الاعتذار:
{excuse_link}
"""

        send_mail(
            "تنبيه خدمة",
            message,
            "nardinmelad015@gmail.com",
            [schedule.servant.email],
            fail_silently=False,
        )

        print(f"Email sent to: {schedule.servant.email}")

        sent_count += 1

    print("=" * 50)
    print("Total Sent:", sent_count)
    print("=" * 50)

    return HttpResponse(
        f"تم إرسال {sent_count} تنبيه لاجتماع {meeting}"
    )



def confirm_schedule(request, schedule_id):

    schedule = get_object_or_404(
        Schedule,
        id=schedule_id
    )

    if schedule.confirmation_status == "confirmed":
        return render(
            request,
            "attendance/already_confirmed.html"
        )

    if schedule.confirmation_status == "excused":
        return render(
            request,
            "attendance/already_excused.html"
        )

    schedule.confirmation_status = "confirmed"
    schedule.save()

    return render(
        request,
        "attendance/confirmed.html"
    )


def excuse_schedule(request, schedule_id):

    schedule = get_object_or_404(
        Schedule,
        id=schedule_id
    )

    if schedule.confirmation_status == "excused":
        return render(
            request,
            "attendance/already_excused.html"
        )

    if schedule.confirmation_status == "confirmed":
        return render(
            request,
            "attendance/already_confirmed.html"
        )

    if request.method == "POST":

        reason = request.POST.get("reason")

        Excuse.objects.create(
            servant=schedule.servant,
            meeting=schedule.meeting,
            reason=reason
        )

        schedule.confirmation_status = "excused"
        schedule.save()

        return render(
            request,
            "attendance/excused_success.html"
        )

    return render(
        request,
        "attendance/excuse_form.html",
        {
            "schedule": schedule
        }
    )
@login_required
def edit_servant(request, servant_id):
    servant = get_object_or_404(Servant, id=servant_id)

    if request.method == "POST":
        form = ServantForm(request.POST, instance=servant)
        if form.is_valid():
            form.save()
            return redirect("servant_list")
    else:
        form = ServantForm(instance=servant)

    return render(
        request,
        "attendance/edit_servant.html",
        {"form": form, "servant": servant}
    )

@login_required
def delete_servant(request, servant_id):
    servant = get_object_or_404(Servant, id=servant_id)

    if request.method == "POST":
        servant.delete()
        return redirect("servant_list")

    return render(
        request,
        "attendance/delete_servant.html",
        {"servant": servant}
    )

@login_required

def meeting_checkin(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
    )

    if request.method == "POST":

        form = CheckInForm(request.POST)

        if form.is_valid():

            servant = form.cleaned_data["servant"]
            attendance_exists = Attendance.objects.filter(
                servant = servant,
                meeting =meeting
            ).exists()

            if attendance_exists:
                return render(
                    request,
                    "attendance/already_checked.html",
                    {
                        "servant":servant,
                        "meeting":meeting
                    }
                )
            Attendance.objects.create(
                servant=servant,
                meeting=meeting,
                status="present"
            )

            return render(
                request,
                "attendance/checkin_success.html",
                {
                    "servant": servant,
                    "meeting": meeting
                }
            )

    else:

        form = CheckInForm()

    return render(
        request,
        "attendance/checkin.html",
        {
            "form": form,
            "meeting": meeting
        }
    )

@login_required

def meeting_qr(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        id=meeting_id
    )

    qr = qrcode.make(
        f"http://192.168.100.6:8000/meeting/{meeting.id}/checkin/"
    )

    response = HttpResponse(
        content_type="image/png"
    )

    qr.save(response, "PNG")

    return response

@login_required
def add_meeting(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)

        print(request.POST)      
        print(form.errors)       

        if form.is_valid():
            form.save()
            return redirect("meeting_list")

    else:
        form = MeetingForm()

    return render(request, "attendance/add_meeting.html", {"form": form})

@login_required
def meeting_list(request):

    meetings = Meeting.objects.all().order_by("-date")

    return render(
        request,
        "attendance/meeting_list.html",
        {
            "meetings": meetings
        }
    )

@login_required

def servant_qr(request, servant_id):

    servant = get_object_or_404(
        Servant,
        id=servant_id
    )

    qr = qrcode.make(
        f"http://127.0.0.1:8000/servant/{servant.id}/"
    )

    response = HttpResponse(
        content_type="image/png"
    )

    qr.save(response, "PNG")

    return response

@login_required

def add_schedule(request):

    if request.method == "POST":
        form = ScheduleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/schedule/add/")

    else:
        form = ScheduleForm()

    return render(
        request,
        "attendance/add_schedule.html",
        {
            "form": form
        }
    )

@login_required

def schedule_list(request):

    schedules = Schedule.objects.all()

    return render(
        request,
        "attendance/schedule_list.html",
        {
            "schedules": schedules
        }
    )

@login_required
def servant_list(request):

    servants_data = []

    for servant in Servant.objects.all():

        attendances = Attendance.objects.filter(servant=servant)

        present = attendances.filter(status="present").count()
        absent = attendances.filter(status="absent").count()
        late = attendances.filter(status="late").count()

        total = present + absent + late

        if total:
            attendance_rate = round((present / total) * 100, 1)
        else:
            attendance_rate = 0

        servant.attendance_rate = attendance_rate

        servants_data.append(servant)

    return render(
        request,
        "attendance/servants_list.html",
        {
            "servants": servants_data
        }
    )

@login_required

def servant_detail(request, servant_id):

    servant = Servant.objects.get(id=servant_id)

    attendances = Attendance.objects.filter(
        servant=servant
    )

    excuses = Excuse.objects.filter(
        servant=servant
    )

    present_count = attendances.filter(
        status="present"
    ).count()

    absent_count = attendances.filter(
        status="absent"
    ).count()

    late_count = attendances.filter(
        status="late"
    ).count()

    total_records = attendances.count()

    if total_records > 0:
        attendance_rate = round(
            (present_count / total_records) * 100,
            1
        )
    else:
        attendance_rate = 0

    return render(
        request,
        "attendance/servant_detail.html",
        {
            "servant": servant,
            "attendances": attendances,
            "excuses": excuses,
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "attendance_rate": attendance_rate,
        }
    )

@login_required

def excuse_list(request):

    excuses = Excuse.objects.all()

    return render(
        request,
        'attendance/excuse_list.html',
        {
            'excuses': excuses
        }
    )

@login_required
def add_servant(request):
    if request.method == "POST":
        form = ServantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("servant_list")
    else:
        form = ServantForm()

    return render(request, "attendance/add_servant.html", {
        "form": form
    })

@login_required

def add_excuse(request):

    if request.method == "POST":
        form = ExcuseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/excuse/add/')

    else:
        form = ExcuseForm()

    return render(
        request,
        'attendance/add_excuse.html',
        {
            'form': form
        }
    )

@login_required

def home(request):
    servants = Servant.objects.all()

    return render(
        request,
        'attendance/home.html',
        {
            'servants': servants
        }
    )

@login_required

def attendance_list(request):

    attendances = Attendance.objects.all()
    
    return render(
        request,
        'attendance/attendance_list.html',
        {
            'attendances': attendances
        }
    )

@login_required
def dashboard(request):
    meeting_id = request.GET.get("meeting")
    meetings = Meeting.objects.all()

    total_servants = Servant.objects.count()

    attendances = Attendance.objects.all()

    if meeting_id:
        attendances = attendances.filter(
            meeting_id=meeting_id
        )

    present_count = attendances.filter(
        status="present"
    ).count()

    late_count = attendances.filter(
        status="late"
    ).count()

    absent_count = attendances.filter(
        status="absent"
    ).count()

    servants_data = []

    for servant in Servant.objects.all():

        servant_attendances = Attendance.objects.filter(
            servant=servant
        )

        if meeting_id:
            servant_attendances = servant_attendances.filter(
                meeting_id=meeting_id
            )

        present = servant_attendances.filter(
            status="present"
        ).count()

        absent = servant_attendances.filter(
            status="absent"
        ).count()

        late = servant_attendances.filter(
            status="late"
        ).count()

        total = present + absent + late

        if total > 0:
            attendance_rate = round(
                (present / total) * 100,
                1
            )
        else:
            attendance_rate = 0

        if attendance_rate >= 90:
            level = "🥇 Gold"
        elif attendance_rate >= 75:
            level = "🥈 Silver"
        elif attendance_rate >= 50:
            level = "🥉 Bronze"
        else:
            level = "🔹 Beginner"

        servants_data.append({
            "id": servant.id,
            "name": servant.name,
            "present": present,
            "absent": absent,
            "late": late,
            "attendance_rate": attendance_rate,
            "level": level,
        })
    leaders = sorted(
        servants_data,
    key=lambda x: x["attendance_rate"],
    reverse=True
)[:3]
    excuses = Excuse.objects.all().order_by("-submitted_at")
    confirmed_schedules = Schedule.objects.filter(
        confirmation_status="confirmed"
    )

    excused_schedules = Schedule.objects.filter(
        confirmation_status="excused"
    )

    pending_schedules = Schedule.objects.filter(
        confirmation_status="pending"
    )
    schedules = Schedule.objects.all()
    return render(
    request,
    "attendance/dashboard.html",
    {
        "total_servants": total_servants,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "attendances": attendances,
        "servants_data": servants_data,
        "leaders": leaders,
        "meetings": meetings,
        "selected_meeting": meeting_id,
        "excuses": excuses,

        "confirmed_schedules": confirmed_schedules,
        "excused_schedules": excused_schedules,
        "pending_schedules": pending_schedules,
        "schedules": schedules,
    }
)

@login_required

def add_attendance(request):

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/attendance/add/')

    else:
        form = AttendanceForm()

    return render(
        request,
        'attendance/add_attendance.html',
        {
            'form': form
        }
    )