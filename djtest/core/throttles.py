# core/throttles.py

from rest_framework.throttling import AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    scope = "login"
    #rate = "10/minute"  # Allow 10 login attempts per minute for anonymous users