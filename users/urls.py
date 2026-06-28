from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='plan_list'), name='home'),
    path('plans/', views.PlanListView.as_view(), name='plan_list'),
    path('plans/new/', views.PlanCreateView.as_view(), name='plan_create'),
    path('plans/<int:pk>/edit/', views.PlanUpdateView.as_view(), name='plan_update'),
    path('plan/<int:pk>/toggle/',views.PlanToggleCompletedView.as_view(),name='plan_toggle_completed'),
    path('plan/<int:pk>/delete/',views.PlanDeleteView.as_view(),name='plan_delete'),
    path('dashboard/chart-data/',views.DailyReportChartDataView.as_view(),name='daily_report_chart_data'),
    path("dashboard/success-chart/",views.SuccessChartDataView.as_view(),name="success_chart"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/plan-chart/',views.DashboardChartDataView.as_view(),name='dashboard_chart_data'),
    path('register/', views.RegisterView.as_view(),name='register')
   
]