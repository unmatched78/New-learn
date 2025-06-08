from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from apps.tenants.models import TenantAwareModel
from apps.hr_modules.employees.models import Employee

class PayrollProfile(TenantAwareModel, TimeStampedModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='payroll_profile')
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    pay_frequency = models.CharField(max_length=20, choices=(
        ('WEEKLY', _('Weekly')),
        ('BIWEEKLY', _('Bi-weekly')),
        ('MONTHLY', _('Monthly')),
        ('SEMIMONTHLY', _('Semi-monthly')),
    ), default='MONTHLY')
    payment_method = models.CharField(max_length=20, choices=(
        ('BANK', _('Bank Transfer')),
        ('CASH', _('Cash')),
        ('CHECK', _('Check')),
        ('MOBILE', _('Mobile Money')),
    ), default='BANK')
    bank_account = models.JSONField(default=dict, blank=True)
    tax_info = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Payroll Profile")
        verbose_name_plural = _("Payroll Profiles")
    
    def __str__(self):
        return f"{self.employee} - {self.salary} {self.currency}"

class PayrollRun(TenantAwareModel, TimeStampedModel):
    period_start = models.DateField()
    period_end = models.DateField()
    pay_date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ('DRAFT', _('Draft')),
        ('PENDING', _('Pending Approval')),
        ('APPROVED', _('Approved')),
        ('PROCESSED', _('Processed')),
        ('FAILED', _('Failed')),
    ), default='DRAFT')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _("Payroll Run")
        verbose_name_plural = _("Payroll Runs")
        ordering = ["-period_end"]
    
    def __str__(self):
        return f"Payroll for {self.period_end.strftime('%B %Y')}"

class PayrollItem(TenantAwareModel, TimeStampedModel):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='items')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.JSONField(default=dict)  # Breakdown of earnings and deductions
    
    class Meta:
        verbose_name = _("Payroll Item")
        verbose_name_plural = _("Payroll Items")
        unique_together = ('payroll_run', 'employee')
    
    def __str__(self):
        return f"{self.employee} - {self.net_pay}"