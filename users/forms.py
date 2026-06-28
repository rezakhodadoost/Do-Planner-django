import jdatetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Plan

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PlanForm(forms.ModelForm):
    plan_time = forms.TimeField(
        label=" ساعت",
        input_formats=['%H:%M'],
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'type': 'time',
                'class': 'form-control'
            }
        )
    )
    plan_date = forms.CharField(
        label=" تاریخ",
        
        required=True, #Mandatory field

        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"انتخاب تاریخ...",
                "autocomplete": "off", #Disable browser suggestions.
                "dir": "rtl"
            }
        ),

        help_text="تاریخ را به صورت شمسی وارد کنید (سال-ماه-روز)"
    )


    class Meta:
        model = Plan
        fields = [
            'title',
            'description',
            'plan_date',
            'plan_time',
            'result_note'
        ]
        labels = {
            "title": "عنوان",
            "description":'توضیحات',
            'result_note': 'یادداشت'

        }

        widgets = {

            "title": forms.TextInput(
      
                attrs={
                    "class":"form-control",
                    "placeholder":"عنوان برنامه..."
                }
            ),


            "description": forms.Textarea(

                attrs={
                    "class":"form-control",
                    "placeholder":"توضیحات برنامه...",
                    "rows":5
                }
            ),


            "result_note": forms.Textarea(

                attrs={
                    "class":"form-control",
                    "placeholder":"نتیجه یا یادداشت نهایی...",
                    "rows":4
                }
            ),

        }



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        #If the form is in edit mode and already exists.
        if self.instance.pk and self.instance.plan_date:

            jalali = jdatetime.date.fromgregorian(
                date=self.instance.plan_date
            )

            self.initial["plan_date"] = (
                jalali.strftime("%Y-%m-%d")
            )



    def clean_plan_date(self):

        value = self.cleaned_data.get("plan_date")


        if not value:

            raise ValidationError(
                "وارد کردن تاریخ الزامی است."
            )


        try:

            parts = value.strip().split("-")

            #3parts
            if len(parts) != 3:

                raise ValueError



            year, month, day = map(int, parts)




            jalali_date = jdatetime.date(
                year,
                month,
                day
            )



            if year <= 1404:

                raise ValidationError(
                    "سال وارد شده باید 1405 باشد "
                )


            #Converts solar date to Gregorian date.
            return jalali_date.togregorian()



        except (ValueError, TypeError):

            raise ValidationError(
                "فرمت تاریخ اشتباه است. مثال صحیح: 1404-04-02"
            )
        
#Registerform 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]