from flask import Flask, request, render_template, render_template_string, send_from_directory, redirect
import os

app = Flask(__name__)

# Initialize calorie data
calorie_data = {
    'breakfast': [],
    'lunch': [],
    'dinner': [],
    'goal': 2000
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'food' in request.form:
            meal = request.form.get('meal')
            food = request.form.get('food')
            calories = int(request.form.get('calories'))
            if meal in calorie_data:
                calorie_data[meal].append((food, calories))
        elif 'goal' in request.form:
            calorie_data['goal'] = int(request.form.get('goal'))
        return redirect('/')

    # Calculate total calories consumed
    total_calories = sum(item[1] for meal in calorie_data.values() if isinstance(meal, list) for item in meal)
    remaining_calories = calorie_data['goal'] - total_calories

    # Determine goal status
    if total_calories == calorie_data['goal']:
        goal_status = "Goal reached!"
    elif total_calories > calorie_data['goal']:
        goal_status = "Goal surpassed!"
    else:
        goal_status = "Keep going!"

    # Read HTML file content
    with open('index.html', 'r') as file:
        html_content = file.read()

    return render_template_string(
        html_content,
        calorie_data=calorie_data,
        total_calories=total_calories,
        remaining_calories=remaining_calories,
        goal_status=goal_status
    )

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
