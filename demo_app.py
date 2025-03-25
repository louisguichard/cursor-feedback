from flask import Flask, render_template_string
from feedback import FeedbackSystem
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create a feedback system instance
feedback_system = FeedbackSystem(
    exit_on_feedback=True  # Exit the app when receiving feedback
)

# Initialize the feedback system with the Flask app
feedback_system.init_app(app, enable_in_debug=True, enable_in_prod=False)

# Demo template with feedback-trigger class added to the header
DEMO_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback System Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .content {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .instructions {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <!-- Add the feedback-trigger class to enable right-click feedback -->
        <h1 class="feedback-trigger">Feedback System Demo</h1>
        <p>A simple demonstration of the feedback system</p>
    </div>
    
    <div class="content">
        <h2>About This Demo</h2>
        <p>This demo shows how to integrate the feedback system into a Flask application.</p>
        <p>The feedback system allows users to provide feedback or report issues by right-clicking on designated elements.</p>
        <p>The best part is you don't need to include any JavaScript or CSS files - it's all handled automatically!</p>
    </div>
    
    <div class="instructions">
        <h2>Instructions</h2>
        <ol>
            <li>Right-click on the page title "Feedback System Demo" above</li>
            <li>Select "Good" to provide positive feedback or "Report Issue" to report a problem</li>
            <li>If you select "Report Issue", you'll be prompted to enter details</li>
        </ol>
        <p><strong>Note:</strong> In this demo, the application will exit when feedback is submitted.</p>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(DEMO_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
