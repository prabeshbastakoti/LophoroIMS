from .models import AuditLog


def log_action(user, action, instance, changes=""):
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        changes=changes,
    )
