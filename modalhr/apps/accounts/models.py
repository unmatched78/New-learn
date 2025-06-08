# apps/accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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
            self.save(update_fields=['modules_access'])
    
    def revoke_module_access(self, module_name):
        """Revoke access to a module"""
        if module_name in self.modules_access:
            self.modules_access.remove(module_name)
            self.save(update_fields=['modules_access'])
    
    def deactivate(self, reason=None):
        """Deactivate user in tenant"""
        self.status = 'inactive'
        self.is_active = False
        self.left_at = timezone.now()
        self.save(update_fields=['status', 'is_active', 'left_at'])
        
        # Log the deactivation
        UserActivityLog.objects.create(
            user=self.user,
            tenant=self.tenant,
            action='deactivated',
            details={'reason': reason} if reason else {}
        )

class UserProfile(TenantAwareModel):
    """Extended user profile information"""
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    national_id = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    
    # Address Information
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[validate_phone_number]
    )
    emergency_contact_email = models.EmailField(blank=True)
    
    # Additional Information
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'user']),
            models.Index(fields=['national_id']),
        ]
    
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"
    
    def get_full_address(self):
        """Return formatted full address"""
        address_parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state_province,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, address_parts))

class UserSession(TimestampedModel):
    """Track user sessions for security and analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    location_info = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
    logout_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"
    
    def end_session(self):
        """End the session"""
        self.is_active = False
        self.logout_at = timezone.now()
        self.save(update_fields=['is_active', 'logout_at'])
    
    @property
    def duration(self):
        """Calculate session duration"""
        end_time = self.logout_at or timezone.now()
        return end_time - self.created_at

class UserActivityLog(TenantAwareModel):
    """Log user activities for audit trails"""
    
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('profile_update', 'Profile Update'),
        ('permission_change', 'Permission Change'),
        ('role_change', 'Role Change'),
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('suspended', 'Suspended'),
        ('data_export', 'Data Export'),
        ('settings_change', 'Settings Change'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    # Generic foreign key for relating to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['tenant', 'action']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.get_action_display()}"

class UserInvitation(TenantAwareModel):
    """Manage user invitations to join tenants"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=TenantUser.TENANT_ROLE_CHOICES)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField(blank=True)
    
    # Employment details for when invitation is accepted
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    modules_access = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'email']),
            models.Index(fields=['token']),
            models.Index(fields=['status', 'expires_at']),
        ]
        unique_together = ['tenant', 'email', 'status']
    
    def __str__(self):
        return f"Invitation to {self.email} for {self.tenant.name}"
    
    def is_expired(self):
        """Check if invitation is expired"""
        return timezone.now() > self.expires_at
    
    def accept(self, user):
        """Accept the invitation and create TenantUser"""
        if self.is_expired():
            raise ValueError("Invitation has expired")
        
        if self.status != 'pending':
            raise ValueError("Invitation is not pending")
        
        # Create or update TenantUser
        tenant_user, created = TenantUser.objects.get_or_create(
            tenant=self.tenant,
            user=user,
            defaults={
                'role': self.role,
                'employee_id': self.employee_id,
                'department': self.department,
                'job_title': self.job_title,
                'modules_access': self.modules_access,
            }
        )
        
        self.status = 'accepted'
        self.accepted_at = timezone.now()
        self.save(update_fields=['status', 'accepted_at'])
        
        return tenant_user
    
    def cancel(self):
        """Cancel the invitation"""
        self.status = 'cancelled'
        self.save(update_fields=['status'])
    
    def extend_expiry(self, days=7):
        """Extend invitation expiry"""
        self.expires_at = timezone.now() + timezone.timedelta(days=days)
        self.save(update_fields=['expires_at'])

class UserToken(TimestampedModel):
    """Manage various user tokens (password reset, email verification, etc.)"""
    
    TOKEN_TYPES = [
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
        ('phone_verification', 'Phone Verification'),
        ('two_factor_backup', 'Two Factor Backup'),
        ('api_access', 'API Access'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    token_type = models.CharField(max_length=30, choices=TOKEN_TYPES)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'token_type']),
            models.Index(fields=['token']),
            models.Index(fields=['expires_at', 'is_used']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.get_token_type_display()}"
    
    def is_expired(self):
        """Check if token is expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if token is valid (not used and not expired)"""
        return not self.is_used and not self.is_expired()
    
    def use_token(self):
        """Mark token as used"""
        if not self.is_valid():
            raise ValueError("Token is not valid")
        
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])

class UserPreference(TenantAwareModel):
    """Store user preferences and settings"""
    
    PREFERENCE_TYPES = [
        ('notification', 'Notification'),
        ('dashboard', 'Dashboard'),
        ('privacy', 'Privacy'),
        ('display', 'Display'),
        ('security', 'Security'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    preference_type = models.CharField(max_length=20, choices=PREFERENCE_TYPES)
    key = models.CharField(max_length=100)
    value = models.JSONField()
    is_system_default = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['tenant', 'user', 'preference_type', 'key']
        indexes = [
            models.Index(fields=['user', 'preference_type']),
            models.Index(fields=['tenant', 'preference_type']),
        ]
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.preference_type}: {self.key}"

class UserDevice(TenantAwareModel):
    """Track user devices for security and 2FA"""
    
    DEVICE_TYPES = [
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('laptop', 'Laptop'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255, unique=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    is_trusted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)
    device_info = models.JSONField(default=dict, blank=True)
    
    # 2FA related
    two_factor_secret = models.CharField(max_length=255, blank=True)
    backup_tokens = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['device_id']),
            models.Index(fields=['last_used']),
        ]
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.device_name}"
    
    def trust_device(self):
        """Mark device as trusted"""
        self.is_trusted = True
        self.save(update_fields=['is_trusted'])
    
    def revoke_trust(self):
        """Revoke device trust"""
        self.is_trusted = False
        self.save(update_fields=['is_trusted'])