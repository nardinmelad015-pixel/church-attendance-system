from django import forms
from .models import Attendance
from .models import Excuse
from .models import Schedule
from .models import Servant
from .models import  Meeting

class ServantForm(forms.ModelForm):
    class Meta:
        model = Servant
        fields = "__all__"

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = "__all__"

class CheckInForm(forms.Form):

    servant = forms.ModelChoiceField(
        queryset=Servant.objects.all(),
        label="اختر اسمك"
    )
    
class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = "__all__"

class ExcuseForm(forms.ModelForm):
    class Meta:
        model = Excuse
        fields = ['servant', 'meeting', 'reason']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'servant',
            'meeting',
            'status'
        ]