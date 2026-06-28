def generate_feedback(success_percentage):

    if success_percentage >= 90:
        return "عملکرد امروز بسیار عالی بوده است."

    elif success_percentage >= 70:
        return "عملکرد امروز خوب بوده است."

    elif success_percentage >= 50:
        return "عملکرد متوسط بوده و جای پیشرفت وجود دارد."

    else:
        return "بخش زیادی از برنامه‌های امروز انجام نشده‌اند."