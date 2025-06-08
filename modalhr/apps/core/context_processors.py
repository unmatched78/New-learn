# apps/core/context_processors.py
def tenant_context(request):
    """Add tenant context to templates"""
    context = {}
    if hasattr(request, 'tenant') and request.tenant:
        context['current_tenant'] = request.tenant
    return context

def module_context(request):
    """Add module context to templates"""
    context = {}
    if hasattr(request, 'tenant') and request.tenant:
        from apps.module_manager.utils import get_active_modules
        context['active_modules'] = get_active_modules(request.tenant)
    return context