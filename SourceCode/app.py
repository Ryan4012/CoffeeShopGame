from flask import Flask , render_template_string
import json

app = Flask(__name__)

@app.route("/")
def sales_dashboard():
    with open("sales.json", "r") as f:
        data = json.load(f)

    total_cups = sum(s["cups_sold"] for s in data)
    total_revenue = sum(s["cups_sold"] * s["cup_price"] for s in data)

    return render_template_string("""
        <h1> Coffee Shop Sales Dashboard</h1>
        <p>Total Cups Sold: <strong>{{ total_cups }}</strong></p>
        <p>Total Revenue: <strong>${{ total_revenue }}</strong></p>
        <hr>
        <h2>Daily Breakdown</h2>
        <ul>
        {% for day in data %}
            <li>Day {{ day.day }} - {{ day.cups_sold }} cups sold @ ${{ day.cup_price }} (Temp: {{ day.temp }}°F)</li>
        {% endfor %}
        </ul>
    """, data=data, total_cups=total_cups, total_revenue=total_revenue)

if __name__ == "__main__":
    app.run(debug=True)

