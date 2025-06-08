from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import TenantAwareModel
from apps.accounts.models import User

class Department(TenantAwareModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    cost_center = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class Employee(TenantAwareModel, TimeStampedModel):
    EMPLOYMENT_TYPES = (
        ('FULL_TIME', _('Full-time')),
        ('PART_TIME', _('Part-time')),
        ('CONTRACTOR', _('Contractor')),
        ('INTERN', _('Intern')),
        ('FREELANCE', _('Freelancer')),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    work_schedule = models.JSONField(default=dict)
    custom_fields = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ["user__last_name", "user__first_name"]
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class EmergencyContact(TenantAwareModel, TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Emergency Contact")
        verbose_name_plural = _("Emergency Contacts")
    
    def __str__(self):
        return f"{self.name} ({self.relationship})"