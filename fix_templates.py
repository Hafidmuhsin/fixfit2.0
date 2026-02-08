import re

# Read the file
with open(r'e:\fixfit2.0\templates\dashboard\profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all the comparison operators
content = re.sub(r"user\.gender=='M'", "user.gender == 'M'", content)
content = re.sub(r"user\.gender=='F'", "user.gender == 'F'", content)
content = re.sub(r"user\.gender=='O'", "user.gender == 'O'", content)
content = re.sub(r"goal\.primary_goal=='lose_weight'", "goal.primary_goal == 'lose_weight'", content)
content = re.sub(r"goal\.primary_goal=='maintain'", "goal.primary_goal == 'maintain'", content)
content = re.sub(r"goal\.primary_goal=='gain_muscle'", "goal.primary_goal == 'gain_muscle'", content)
content = re.sub(r"goal\.activity_level=='sedentary'", "goal.activity_level == 'sedentary'", content)
content = re.sub(r"goal\.activity_level=='lightly_active'", "goal.activity_level == 'lightly_active'", content)
content = re.sub(r"goal\.activity_level=='moderately_active'", "goal.activity_level == 'moderately_active'", content)
content = re.sub(r"goal\.activity_level=='very_active'", "goal.activity_level == 'very_active'", content)

# Fix widthratio filter
content = re.sub(r'\{\{\s*bmi\|widthratio:40:100\s*\}\}', '{{ bmi_percent }}', content)

# Write to both files
with open(r'e:\fixfit2.0\templates\dashboard\profile_final.html', 'w', encoding='utf-8') as f:
    f.write(content)
    
with open(r'e:\fixfit2.0\templates\dashboard\profile.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed both profile.html and profile_final.html')
