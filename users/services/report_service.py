from django.utils import timezone
from ..models import Plan

def calculate_daily_success(user):
    plans = Plan.objects.filter(
        created_by=user,
        plan_date__lte=timezone.now().date()
    )

    total = plans.count()

    if total == 0:
        return 0

    completed = plans.filter(completed=True).count()

    return round((completed / total) * 100)