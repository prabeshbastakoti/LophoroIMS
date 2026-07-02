from .models import User


def is_last_active_admin(user) -> bool:
    """True if `user` is currently an active Admin and no other active Admin exists."""
    if user.role != "ADMIN" or not user.is_active:
        return False
    other_active_admins = User.objects.filter(role="ADMIN", is_active=True).exclude(pk=user.pk)
    return not other_active_admins.exists()
