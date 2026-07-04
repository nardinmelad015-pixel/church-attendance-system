from django.db import models


class Servant(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(
    blank=True,
    null=True
)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    
    def __str__(self):
        return self.title
    
    


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
    ]

    servant = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE
    )

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    check_in_time = models.DateTimeField(
        null=True,
        blank=True
    )

class Schedule(models.Model):

    servant = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE
    )

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE
    )

    task = models.CharField(
        max_length=100
    )

    notes = models.TextField(
        blank=True
    )

    TASK_STATUS = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]

    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS,
        default="pending"
    )

    CONFIRMATION_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("declined", "Declined"),
    ]

    confirmation_status = models.CharField(
        max_length=20,
        choices=CONFIRMATION_CHOICES,
        default="pending"
    )
class Excuse(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    CONFIRMATION_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("excused", "Excused"),
    ]

    confirmation_status = models.CharField(
    max_length=20,
    choices=CONFIRMATION_CHOICES,
    default="pending"
)

    servant = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE
    )

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )