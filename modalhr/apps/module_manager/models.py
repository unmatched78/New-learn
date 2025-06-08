from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import TenantAwareModel, Tenant

class ModuleRegistry(TimeStampedModel):
    MODULE_CATEGORIES = (
        ('CORE', _('Core HR')),
        ('PAYROLL', _('Payroll')),
        ('TIME', _('Time & Attendance')),
        ('BENEFITS', _('Benefits')),
        ('PERF', _('Performance')),
        ('RECRUIT', _('Recruitment')),
        ('LEARNING', _('Learning & Development')),
    )
    
    name = models.CharField(max_length=100)
    codename = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=MODULE_CATEGORIES)
    version = models.CharField(max_length=20, default='1.0.0')
    dependencies = ArrayField(models.SlugField(), default=list, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Module Registry")
        verbose_name_plural = _("Module Registry")
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class TenantModule(TenantAwareModel, TimeStampedModel):
    module = models.ForeignKey(ModuleRegistry, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = _("Tenant Module")
        verbose_name_plural = _("Tenant Modules")
        unique_together = ('tenant', 'module')
    
    def __str__(self):
        return f"{self.tenant.name} - {self.module.name}"