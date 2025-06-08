# HRMIS – Django Human Resource Management Information System

A modular, multi-tenant HR platform built with Django and Django REST Framework. Designed for SaaS-style deployment, HRMIS allows organizations (tenants) to pick and choose core HR features—such as employee profiles, time tracking, leave management, and payroll—while ensuring complete data isolation per tenant. Built-in tools include JWT authentication, background task processing with Celery/Redis, PostgreSQL schema-based multi-tenancy, and a streamlined developer experience.

---

## 🧩 What This Project Provides

1. **Modular HR Functionality**  
   - Apps for Accounts, Employees, Payroll, Time Attendance, Leave Management, Performance, Recruitment, Benefits, Learning.  
   - Each module has its own models, views, serializers, and URL routes.

2. **Multi-Tenant Architecture**  
   - Isolated data using separate PostgreSQL schemas with `django-tenant-schemas` or `django-tenant-users`.  
   - Central `public` schema for shared models, and per-tenant schemas for HR data.

3. **RESTful API**  
   - Built using Django REST Framework.  
   - Offers browsable API, custom permissions, pagination, and error handling.

4. **Secure Authentication**  
   - JWT-based auth via `djangorestframework-simplejwt`.  
   - Token rotation, blacklisting, and standard auth endpoints.

5. **Asynchronous Processing**  
   - Background jobs handled by Celery with Redis as broker.  
   - Features scheduled tasks like payroll processing, document expiry checks, and notifications.

6. **Developer Experience Enhancements**  
   - Django Debug Toolbar for performance insights during development.  
   - `shell_plus` from `django-extensions` for interactive model exploration.  
   - Structured code for signals, middleware, audit logging, and shared utilities.

- **License & contribution guidelines**
