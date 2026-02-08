# 🚀 FIX-FIT: Real Feature Implementation Plan

## 1. 🎯 Dynamic Goal System
To make goals "real" and adjustable, we need a dedicated place to store them.
- **Model**: `UserGoal` in `achievements` app.
  - `daily_calorie_goal` (default: 2000 kcal)
  - `water_goal_ml` (default: 2500 ml)
  - `sleep_goal_hours` (default: 8.0)
  - `weight_goal_kg` (target weight)

## 2. 🍎 Food & Calorie Logic
- **Food Database**: Pre-populate `FoodItem` with common foods (Seed data).
- **Logging Interface**:
  - View: `add_food/`
  - Logic: Search `FoodItem` or enter custom.
  - Calculation: Update "Calories Consumed" progress bar in real-time.

## 3. 🏋️ Exercise & Burn Rate
- **Burn Rate Logic**: `ExerciseType` model needs `calories_per_minute` (or METs).
- **Dynamic Goals**:
  - `Net Calories` = `Food Intake` - `Exercise Burn`.
  - If user exercises, their "Available Calories" increases.

## 4. 💧 Water Monitoring
- **Quick Actions**: "Add Cup (250ml)", "Add Bottle (500ml)" buttons on dashboard.
- **Logic**: Immediate update of water progress bar vs `water_goal_ml`.

## 5. 😴 Sleep Scheduling
- **Monitoring**: Log Bedtime / Wake time -> auto-calculate Duration.
- **Quality**: User rates 1-10.

---

## 🛠️ Execution Steps

### Phase A: Models & Data (Backend)
1.  Create `UserGoal` model.
2.  Update `FoodItem` and `ExerciseType` models with necessary math fields.
3.  Migrate database.

### Phase B: Goal Settings (Frontend)
1.  Create "Settings" page to let user change their goals.
2.  Update Dashboard to use *dynamic* `UserGoal` instead of hardcoded 2500.

### Phase C: Add/Log Forms (Interactivity)
1.  Create `log_food` view & template.
2.  Create `log_exercise` view & template (with burn calc).
3.  Create `log_water` (HTMX/AJAX or simple link).
4.  Create `log_sleep` view.

### Phase D: Dynamic Dashboard Logic
1.  Update `views.py` to calculate:
    - `Calories In` (Food)
    - `Calories Out` (Exercise)
    - `Net Remaining` = `Goal - In + Out`
