from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import TenantAwareModel
from apps.hr_modules.employees.models import Employee

class AttendanceRecord(TenantAwareModel, TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=50, choices=(
        ('WEB', _('Web')),
        ('MOBILE', _('Mobile')),
        ('BIOMETRIC', _('Biometric')),
        ('API', _('API')),
    ), default='WEB')
    status = models.CharField(max_length=20, choices=(
        ('PRESENT', _('Present')),
        ('LATE', _('Late')),
        ('ABSENT', _('Absent')),
        ('HOLIDAY', _('Holiday')),
    ), default='PRESENT')
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _("Attendance Record")
        verbose_name_plural = _("Attendance Records")
        ordering = ["-clock_in"]
    
    def __str__(self):
        return f"{self.employee} - {self.clock_in.date()}"

class Shift(TenantAwareModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.DurationField(null=True, blank=True)
    days = ArrayField(models.IntegerField(), size=7)  # 0=Sunday, 1=Monday, etc.
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")
        ordering = ["start_time"]
    
    def __str__(self):
        return self.name

class OvertimeRequest(TenantAwareModel, TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('PENDING', _('Pending')),
        ('APPROVED', _('Approved')),
        ('REJECTED', _('Rejected')),
    ), default='PENDING')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_overtimes')
    
    class Meta:
        verbose_name = _("Overtime Request")
        verbose_name_plural = _("Overtime Requests")
    
    def __str__(self):
        return f"{self.employee} - {self.date}"