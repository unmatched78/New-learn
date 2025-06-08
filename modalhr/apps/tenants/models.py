from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, SoftDeleteModel, Country

class Tenant(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=50, unique=True)
    legal_name = models.CharField(max_length=200, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    address = models.JSONField(default=dict)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    trial_end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, editable=False)
    
    class Meta:
        abstract = True

class TenantConfiguration(TimeStampedModel):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='config')
    payroll_settings = models.JSONField(default=dict)
    attendance_settings = models.JSONField(default=dict)
    leave_settings = models.JSONField(default=dict)
    notification_settings = models.JSONField(default=dict)
    localization_settings = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = _("Tenant Configuration")
        verbose_name_plural = _("Tenant Configurations")
    
    def __str__(self):
        return f"Config for {self.tenant.name}"