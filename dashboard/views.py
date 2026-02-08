from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from django.conf import settings
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt

# Models
from nutrition.models import CalorieLog, FoodItem
from hydration.models import WaterIntake
from sleep.models import SleepLog
from exercise.models import ExerciseLog, ExerciseType
from achievements.models import UserGoal

# Forms
from .forms import GoalForm, FoodLogForm, WaterLogForm, ExerciseLogForm, SleepLogForm, ProfileUpdateForm, ProfileAnalysisForm, GoalAnalysisForm

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'dashboard/index.html')

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    goal, created = UserGoal.objects.get_or_create(user=request.user)
    
    # Aggregation
    calories_in = CalorieLog.objects.filter(user=request.user, created_at__date=today).aggregate(Sum('calories'))['calories__sum'] or 0
    calories_out = ExerciseLog.objects.filter(user=request.user, created_at__date=today).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    net_calories = calories_in - calories_out
    
    water_ml = WaterIntake.objects.filter(user=request.user, created_at__date=today).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
    
    sleep_log = SleepLog.objects.filter(user=request.user, created_at__date=today).last()
    sleep_minutes = sleep_log.duration_minutes if sleep_log else 0
    sleep_hours_display = f"{sleep_minutes // 60}h {sleep_minutes % 60}m"
    
    exercise_minutes = ExerciseLog.objects.filter(user=request.user, created_at__date=today).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0

    # Percentages
    cal_goal = goal.daily_calories or 2000
    water_goal = goal.daily_water_ml or 2500
    sleep_goal_mins = float(goal.daily_sleep_hours) * 60 if goal.daily_sleep_hours else 480
    
    adjusted_cal_goal = cal_goal + calories_out
    cal_percent = min(int((calories_in / adjusted_cal_goal) * 100), 100) if adjusted_cal_goal > 0 else 0
    
    water_percent = min(int((water_ml / water_goal) * 100), 100) if water_goal > 0 else 0
    sleep_percent = min(int((sleep_minutes / sleep_goal_mins) * 100), 100) if sleep_goal_mins > 0 else 0
    
    recent_cals = CalorieLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_water = WaterIntake.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_exercise = ExerciseLog.objects.filter(user=request.user).order_by('-created_at')[:3]

    context = {
        'goal': goal,
        'calories_in': calories_in,
        'calories_out': calories_out,
        'net_calories': net_calories,
        'remaining_calories': adjusted_cal_goal - calories_in,
        'adjusted_cal_goal': adjusted_cal_goal,
        'cal_percent': cal_percent,
        
        'water_ml': water_ml,
        'water_percent': water_percent,
        
        'sleep_hours_display': sleep_hours_display,
        'sleep_percent': sleep_percent,
        
        'exercise_minutes': exercise_minutes,
        
        'recent_cals': recent_cals,
        'recent_water': recent_water,
        'recent_exercise': recent_exercise,
        
        'today_food_items': FoodItem.objects.all().order_by('name'),
        'exercise_types': ExerciseType.objects.all(),
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def log_food(request):
    if request.method == 'POST':
        user = request.user
        food_id = request.POST.get('food_id')
        custom_name = request.POST.get('custom_name')
        calories = request.POST.get('calories')
        meal_type = request.POST.get('meal_type', 'Snack')
        
        if food_id:
            food = get_object_or_404(FoodItem, id=food_id)
            CalorieLog.objects.create(user=user, food_item=food, food_name=food.name, calories=food.calories, meal_type=meal_type)
            messages.success(request, f"Logged {food.name}")
        elif custom_name and calories:
            CalorieLog.objects.create(user=user, food_name=custom_name, calories=int(calories), meal_type=meal_type)
            messages.success(request, f"Logged {custom_name}")
            
    return redirect('dashboard')

@login_required
def log_water(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 250))
        WaterIntake.objects.create(user=request.user, amount_ml=amount)
        messages.success(request, f"Added {amount}ml water")
    return redirect('dashboard')

@login_required
def log_exercise(request):
    if request.method == 'POST':
        exercise_type_id = request.POST.get('exercise_type')
        duration = int(request.POST.get('duration', 30))
        intensity = request.POST.get('intensity', 'Medium')
        
        log = ExerciseLog(user=request.user, duration_minutes=duration, intensity=intensity)
        
        if exercise_type_id:
            ex_type = get_object_or_404(ExerciseType, id=exercise_type_id)
            log.exercise_type = ex_type
            # Calculation handled in model save()
        else:
            cals = request.POST.get('calories_burned')
            name = request.POST.get('activity_name', 'Custom Workout')
            log.activity_name = name
            if cals: log.calories_burned = int(cals)
            else: log.calories_burned = duration * 5
                 
        log.save()
        messages.success(request, "Workout logged!")
    return redirect('dashboard')

@login_required
def log_sleep(request):
    if request.method == 'POST':
        duration = int(request.POST.get('duration', 480))
        quality = int(request.POST.get('quality', 7))
        SleepLog.objects.create(user=request.user, duration_minutes=duration, quality=quality)
        messages.success(request, "Sleep logged!")
    return redirect('dashboard')

@login_required
def update_goals(request):
    if request.method == 'POST':
        goal, _ = UserGoal.objects.get_or_create(user=request.user)
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goals updated successfully!")
        else:
            messages.error(request, "Error updating goals.")
    return redirect('dashboard')

@login_required
def delete_log(request, log_type, log_id):
    if request.method == 'POST':
        try:
            if log_type == 'food': CalorieLog.objects.filter(id=log_id, user=request.user).delete()
            elif log_type == 'exercise': ExerciseLog.objects.filter(id=log_id, user=request.user).delete()
            elif log_type == 'water': WaterIntake.objects.filter(id=log_id, user=request.user).delete()
            messages.success(request, "Log deleted.")
        except Exception as e:
            messages.error(request, "Error deleting log.")
    return redirect('dashboard')

# --- Profile & AI ---

def calculate_age(born):
    if not born: return 0
    today = timezone.now().date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@login_required
def profile_view(request):
    user = request.user
    goal, _ = UserGoal.objects.get_or_create(user=user)
    
    # Defaults
    bmi = 0
    bmi_category = "N/A"
    bmr = 0
    tdee = 0
    target_calories = goal.daily_calories
    suggestion = "Update your profile details to get personalized insights."
    
    if user.weight and user.height and user.date_of_birth and user.gender:
        # BMI
        height_m = float(user.height) / 100
        weight_kg = float(user.weight)
        if height_m > 0:
            bmi = round(weight_kg / (height_m * height_m), 1)
        
        if bmi < 18.5: bmi_category = "Underweight"
        elif bmi < 25: bmi_category = "Normal Weight"
        elif bmi < 30: bmi_category = "Overweight"
        else: bmi_category = "Obese"
            
        # BMR (Mifflin-St Jeor)
        age = calculate_age(user.date_of_birth)
        if user.gender == 'M':
            bmr = (10 * weight_kg) + (6.25 * float(user.height)) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * float(user.height)) - (5 * age) - 161
            
        # TDEE
        multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725
        }
        activity_factor = multipliers.get(goal.activity_level, 1.2)
        tdee = int(bmr * activity_factor)
        
        # Goal Adjustment Suggestion
        if goal.primary_goal == 'lose_weight':
            target_calories = tdee - 500
            suggestion = "To lose weight safely (0.5kg/week), aim for a 500 calorie deficit daily."
        elif goal.primary_goal == 'gain_muscle':
            target_calories = tdee + 250
            suggestion = "To gain muscle, consume a surplus of 250-500 calories along with resistance training."
        else:
            target_calories = tdee
            suggestion = "Maintain your current weight by matching your intake to your calculated expenditure."
            
    context = {
        'goal': goal,
        'bmi': bmi,
        'bmi_category': bmi_category,
        'tdee': tdee,
        'bmr': int(bmr),
        'bmi_percent': min(int((bmi / 40) * 100), 100) if bmi else 0,
        'suggested_calories': int(target_calories) if tdee else 0,
        'suggestion': suggestion,
        'profile_form': ProfileAnalysisForm(instance=request.user),
        'goal_form': GoalAnalysisForm(instance=goal)
    }
    print("Loading Profile View FINAL")
    return render(request, 'dashboard/profile.html', context)

@login_required
def update_profile_details(request):
    if request.method == 'POST':
        # Update User
        p_form = ProfileAnalysisForm(request.POST, instance=request.user)
        # Update Goal (Activity)
        goal, _ = UserGoal.objects.get_or_create(user=request.user)
        g_form = GoalAnalysisForm(request.POST, instance=goal)
        
        if p_form.is_valid() and g_form.is_valid():
            p_form.save()
            g_form.save()
            messages.success(request, "Analysis updated successfully.")
        else:
            messages.error(request, "Error updating profile.")
            
    return redirect('profile')

@login_required
def assistant_view(request):
    return render(request, 'dashboard/assistant.html')

@login_required
def chart_data(request):
    today = timezone.now().date()
    
    labels = []
    cals_data = []
    water_data = []
    sleep_data = []
    
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime('%a'))
        
        # Calories
        c = CalorieLog.objects.filter(user=request.user, created_at__date=d).aggregate(Sum('calories'))['calories__sum'] or 0
        cals_data.append(c)
        
        # Water
        water_sum = WaterIntake.objects.filter(user=request.user, created_at__date=d).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
        water_data.append(water_sum)
        
        # Sleep
        sleep_log = SleepLog.objects.filter(user=request.user, created_at__date=d).first()
        sleep_mins = sleep_log.duration_minutes if sleep_log else 0
        sleep_data.append(round(sleep_mins / 60, 1))
        
    return JsonResponse({
        'labels': labels,
        'calories': cals_data,
        'water': water_data,
        'sleep': sleep_data
    })

@csrf_exempt
@login_required
def ask_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message defined'}, status=400)
                
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                return JsonResponse({
                    'answer': "I'm currently running in dummy mode because the API Key is missing. Please add GEMINI_API_KEY to your .env file."
                })
                
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            user = request.user
            goal, _ = UserGoal.objects.get_or_create(user=user)
            
            prompt = f"""
            Role: You are 'FitBot', a highly motivating and knowledgeable personal health coach.
            User Context:
            - Name: {user.first_name or user.username}
            - Goal: {goal.get_primary_goal_display()} ({goal.target_weight}kg)
            - Activity Level: {goal.get_activity_level_display()}
            - Daily Calories: {goal.daily_calories} kcal
            
            Question: "{user_message}"
            
            Response Guidelines:
            - Be concise (max 3 sentences unless detailed explanation needed).
            - Be encouraging.
            - Use emojis sparingly.
            - Focus on actionable advice related to their specific goal.
            """
            
            response = model.generate_content(prompt)
            return JsonResponse({'answer': response.text})
            
        except Exception as e:
            print(f"AI ERROR: {str(e)}")
            return JsonResponse({'answer': f"Sorry, I encountered an error: {str(e)}"}, status=500)
            
    return JsonResponse({'error': 'Invalid method'}, status=405)
