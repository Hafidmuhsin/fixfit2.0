from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Action URLs
    path('log/food/', views.log_food, name='log_food'),
    path('log/water/', views.log_water, name='log_water'),
    path('log/exercise/', views.log_exercise, name='log_exercise'),
    path('log/sleep/', views.log_sleep, name='log_sleep'),
    
    path('goals/update/', views.update_goals, name='update_goals'),
    path('delete/<str:log_type>/<int:log_id>/', views.delete_log, name='delete_log'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_details, name='update_profile'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
    path('api/ask-ai/', views.ask_ai, name='ask_ai'),
    path('assistant/', views.assistant_view, name='assistant'),
]
