from flask import Flask, request, jsonify, render_template_string
import pickle
import pandas as pd
from datetime import datetime, timedelta

# Load the fitted SARIMA model
with open("arima_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Oil Price Forecasting</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="number"] { width: 100px; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
        .forecast-item { margin: 5px 0; padding: 5px; background: white; border-radius: 3px; }
        .error { color: red; background: #ffe6e6; padding: 10px; border-radius: 4px; }
        .chart-container { margin: 20px 0; height: 400px; }
        .data-section { display: flex; gap: 20px; }
        .chart-section { flex: 2; }
        .values-section { flex: 1; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>Oil Price Forecasting</h1>
        
        <form method="GET" action="/">
            <div class="form-group">
                <label for="steps">Number of Forecast Steps:</label>
                <input type="number" id="steps" name="steps" value="{{ request.args.get('steps', '12') }}" min="1" max="100" required>
                <button type="submit">Get Forecast</button>
            </div>
        </form>

        {% if forecast_data %}
        <div class="result">
            <h3>Forecast Results ({{ forecast_data.steps }} steps)</h3>
            <p><strong>Min Value:</strong> {{ "%.2f"|format(forecast_data.min_value) }}</p>
            <p><strong>Max Value:</strong> {{ "%.2f"|format(forecast_data.max_value) }}</p>
            <p><strong>Mean Value:</strong> {{ "%.2f"|format(forecast_data.mean_value) }}</p>
            
            <div class="data-section">
                <div class="chart-section">
                    <h4>Forecast Chart:</h4>
                    <div class="chart-container">
                        <canvas id="forecastChart"></canvas>
                    </div>
                </div>
                
                <div class="values-section">
                    <h4>Forecast Values:</h4>
                    <div style="max-height: 300px; overflow-y: auto;">
                        {% for month, value in forecast_data['values'] %}
                        <div class="forecast-item">
                            <strong>{{ month }}:</strong> {{ "%.2f"|format(value) }}
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            
            <script>
                const ctx = document.getElementById('forecastChart').getContext('2d');
                const chartData = {
                    labels: {{ forecast_data['values'] | map(attribute=0) | list | tojson }},
                    datasets: [{
                        label: 'Oil Price Forecast',
                        data: {{ forecast_data['values'] | map(attribute=1) | list | tojson }},
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1,
                        fill: true
                    }]
                };
                
                new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Oil Price Time Series Forecast'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: false,
                                title: {
                                    display: true,
                                    text: 'Price'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Month'
                                }
                            }
                        }
                    }
                });
            </script>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">
            <strong>Error:</strong> {{ error }}
        </div>
        {% endif %}
    </div>
    <footer style="text-align:center; margin-top:40px; color:#888; font-size:16px;">
        <hr style="margin:30px 0;">
        <p>View the project on <a href="https://github.com/msarvesh2022/Oil-Price" target="_blank" style="color:#007bff; text-decoration:underline;">GitHub</a></p>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    steps_param = request.args.get('steps', '12')

    if not steps_param:
        return render_template_string(HTML_TEMPLATE)

    try:
        steps = int(steps_param)
        if steps <= 0 or steps > 100:
            return render_template_string(HTML_TEMPLATE, error="Steps must be between 1 and 100")

        # Forecast
        forecast_values = model.forecast(steps=steps)

        # Convert to list
        if hasattr(forecast_values, 'tolist'):
            forecast_list = forecast_values.tolist()
        else:
            forecast_list = list(forecast_values)

        # Generate month names for each step
        current_date = datetime.now()
        month_names = []
        for i in range(steps):
            future_date = current_date + timedelta(days=30*i)  # Approximate month increment
            month_names.append(future_date.strftime("%B %Y"))

        forecast_data = {
            'steps': steps,
            'values': list(zip(month_names, forecast_list)),
            'min_value': float(min(forecast_list)),
            'max_value': float(max(forecast_list)),
            'mean_value': float(sum(forecast_list) / len(forecast_list))
        }

        return render_template_string(HTML_TEMPLATE, forecast_data=forecast_data)

    except ValueError:
        return render_template_string(HTML_TEMPLATE, error="Please enter a valid number")
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error=f"Forecast error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
