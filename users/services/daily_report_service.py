from django.utils import timezone
from ..models import DailyReport
from .report_service import calculate_daily_success
from .ai_service import generate_feedback


def create_daily_report(user):

    today = timezone.now().date()

    success = calculate_daily_success(user)

    feedback = generate_feedback(success)


    DailyReport.objects.update_or_create(
        user=user,
        date=today,
        defaults={
            "success_percentage": success,
            "ai_feedback": feedback
        }
    )