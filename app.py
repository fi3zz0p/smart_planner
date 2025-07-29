from flask import Flask, render_template, request

app = Flask(__name__)

def smart_schedule(tasks, start_hour=9, end_hour=17):
    schedule = []
    current_time = start_hour * 60
    end_time = end_hour * 60
    for task in tasks:
        name = task['name']
        try:
            duration = float(task['duration']) * 60  # ساعت ضربدر 60 = دقیقه
        except ValueError:
            continue  # اگر مدت زمان اشتباه بود رد کن
        if current_time + duration <= end_time:
            start = current_time
            end = current_time + duration
            schedule.append({
                'name': name,
                'start': f"{int(start // 60):02d}:{int(start % 60):02d}",
                'end': f"{int(end // 60):02d}:{int(end % 60):02d}"
            })
            current_time = end
        else:
            break
    return schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tasks = []
        task_names = request.form.getlist('task')
        durations = request.form.getlist('duration')
        for name, duration in zip(task_names, durations):
            if name.strip() and duration.strip():
                tasks.append({'name': name.strip(), 'duration': duration.strip()})
        if tasks:
            result = smart_schedule(tasks)
            return render_template('index.html', schedule=result)
        else:
            return render_template('index.html', schedule=[])
    else:
        return render_template('index.html', schedule=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
