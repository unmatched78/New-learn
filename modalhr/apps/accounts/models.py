# apps/accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from apps.core.models import TimestampedModel, TenantAwareModel
from apps.core.validators import validate_phone_number

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('tenant_admin', 'Tenant Admin'),
        ('hr_manager', 'HR Manager'),
        ('hr_employee', 'HR Employee'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[validate_phone_number]
    )
    
    # Profile Information
    middle_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    
    # System Information
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Security
    two_factor_enabled = models.BooleanField(default=False)
    backup_tokens = models.JSONField(default=list, blank=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    force_password_change = models.BooleanField(default=False)
    login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    notification_preferences = models.JSONField(default=dict, blank=True)
    dashboard_preferences = models.JSONField(default=dict, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active', 'is_verified']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Return the full name of the user"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_display_name(self):
        """Return display name (full name or email if no name)"""
        full_name = self.get_full_name()
        return full_name if full_name else self.email
    
    def verify_email(self):
        """Mark email as verified"""
        self.is_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'email_verified_at'])
    
    def verify_phone(self):
        """Mark phone as verified"""
        self.phone_verified_at = timezone.now()
        self.save(update_fields=['phone_verified_at'])
    
    def is_phone_verified(self):
        """Check if phone is verified"""
        return self.phone_verified_at is not None
    
    def is_account_locked(self):
        """Check if account is locked"""
        if self.locked_until:
            return timezone.now() < self.locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['locked_until'])
    
    def unlock_account(self):
        """Unlock account"""
        self.locked_until = None
        self.login_attempts = 0
        self.save(update_fields=['locked_until', 'login_attempts'])
    
    def increment_login_attempts(self):
        """Increment failed login attempts"""
        self.login_attempts += 1
        if self.login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        self.save(update_fields=['login_attempts'])
    
    def reset_login_attempts(self):
        """Reset login attempts on successful login"""
        self.login_attempts = 0
        self.save(update_fields=['login_attempts'])

class TenantUser(TenantAwareModel):
    """Model to link users to tenants with specific roles"""
    
    TENANT_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr_manager', 'HR Manager'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('contractor', 'Contractor'),
        ('intern', 'Intern'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_users')
    role = models.CharField(max_length=20, choices=TENANT_ROLE_CHOICES, default='employee')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    # Employment Information
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    
    # Access Control
    permissions = models.JSONField(default=dict, blank=True)
    modules_access = models.JSONField(default=list, blank=True)
    
    class Meta:
        unique_together = ['tenant', 'user']
        indexes = [
            models.Index(fields=['tenant', 'user']),
            models.Index(fields=['tenant', 'role']),
            models.Index(fields=['tenant', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.tenant.name} ({self.role})"
    
    def has_module_access(self, module_name):
        """Check if user has access to specific module"""
        return module_name in self.modules_access
    
    def grant_module_access(self, module_name):
        """Grant access to a module"""
        if module_name not in self.modules_access:
            self.modules_access.append(module_name)
            self.save(update_fields=['modules_access']).....