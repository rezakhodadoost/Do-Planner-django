from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Plan, DailyReport
from .forms import PlanForm , RegisterForm
from .services.daily_report_service import create_daily_report
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
#When logged in you can see the plan_list.
class PlanListView(LoginRequiredMixin, ListView):
    model = Plan
    template_name = 'plan_list.html'
    context_object_name = 'plans'
    #This method specifies what data is read from the database.
    def get_queryset(self):
        return Plan.objects.filter(created_by=self.request.user).order_by('-plan_date')

# you can creat plan when you logged in .
class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'plan_form.html'
    success_url = reverse_lazy('plan_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# for updateview.
class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'plan_form.html'
    success_url = reverse_lazy('plan_list')

    def get_queryset(self):
        return Plan.objects.filter(created_by=self.request.user)

# dashboard class.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        #The user who is currently logged in.
        user = self.request.user
        create_daily_report(user)
        report = DailyReport.objects.filter(
            user=user
        ).order_by('-date').first()


        plans = Plan.objects.filter(
            created_by=user
        )
        total = plans.count()

        completed = plans.filter(
            completed=True
        ).count()

        progress = 0

        if total > 0:
            progress = int(
                (completed / total) * 100
            )
        context.update({
            "report": report,
            "total_plans": total,
            "completed_plans": completed,
            "pending_plans": total - completed,
            "progress": progress,

        })
        return context



#But this representation returns a JSON which is commonly used for writing (Chart.js).
class DashboardChartDataView(LoginRequiredMixin,TemplateView):

    def get(self, request, *args, **kwargs):

        plans = Plan.objects.filter(
            created_by=request.user
        )
        completed = plans.filter(
            completed=True
        ).count()
        pending = plans.filter(
            completed=False
        ).count()
        return JsonResponse({

            "labels": [
                "انجام شده",
                "باقی مانده"
            ],


            "values": [
                completed,
                pending
            ]

        })
#This View is for changing the execution status of the program.    
class PlanToggleCompletedView(LoginRequiredMixin, View):
    def post(self, request, pk):
        plan = get_object_or_404(
            Plan,
            pk=pk,
            created_by=request.user
        )
        plan.completed = not plan.completed
        plan.save()
        return redirect('plan_list')
#This view is used to delete a plan.    
class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('plan_list')
    template_name = 'plan_delete.html'

    def get_queryset(self):
        return Plan.objects.filter(
            created_by=self.request.user
        )
#This View is for sending daily report chart data in JSON format.    
class DailyReportChartDataView(LoginRequiredMixin, View):

    def get(self, request):
        reports = DailyReport.objects.filter(
            user=request.user
        ).order_by("date")

        return JsonResponse({
            "labels": [
                r.date.strftime("%Y-%m-%d")
                for r in reports
            ],
            "values": [
                r.success_percentage
                for r in reports
            ]
        })
# Success rate  
class SuccessChartDataView(LoginRequiredMixin, View):

    def get(self, request):

        plans = Plan.objects.filter(
            created_by=request.user
        )


        completed = plans.filter(
            completed=True
        ).count()


        not_completed = plans.filter(
            completed=False
        ).count()


        total = completed + not_completed


        success_percent = 0

        if total > 0:
            success_percent = round(
                (completed / total) * 100
            )


        return JsonResponse({

            "labels": [
                "انجام شده",
                "انجام نشده"
            ],


            "values": [
                completed,
                not_completed
            ],


            "percent": success_percent

        })
#logout    
class LogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login/')
    
#RegisterView
class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

        return render(request, self.template_name, {"form": form})