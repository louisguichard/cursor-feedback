# Cursor Feedback

A lightweight feedback system for Flask applications that allows users to provide feedback by right-clicking on designated elements.

## Why Use This?

I originally created this to reduce the number of API requests when using Cursor Agent mode. By allowing the user to provide feedback directly during a test session, the agent can self-correct without requiring a new request.

## Installation

```bash
pip install git+https://github.com/louisguichard/cursor-feedback.git
```

## Basic Usage

1. Import the feedback system in your Flask application and initialize it:

```python
from flask import Flask
from feedback import FeedbackSystem

app = Flask(__name__)

# Create a feedback system instance
feedback_system = FeedbackSystem()
feedback_system.init_app(app)
```

2. Add the `feedback-trigger` class to elements that should trigger the feedback menu:

```html
<h1 class="feedback-trigger">My Application</h1>
```

That's it! When you right-click on an element with the `feedback-trigger` class, you will see a menu to provide feedback.

## Configuration Options

### FeedbackSystem Class

The `FeedbackSystem` class accepts the following parameter:

- `exit_on_feedback` (default: `True`): Whether to exit the application after sending feedback

### init_app Method

The `init_app` method accepts the following parameters:

- `app`: The Flask application
- `enable_in_debug` (default: `True`): Whether to enable feedback in debug mode
- `enable_in_prod` (default: `False`): Whether to enable feedback in production mode

## How It Works

The feedback system works by:

1. Creating a Flask blueprint with a route to handle feedback submissions
2. Automatically injecting the necessary JavaScript into your HTML responses
3. Adding event listeners to elements with the `feedback-trigger` class
4. Sending feedback to the server when the user submits it

The system doesn't rely on external files or templates - everything is embedded in the response!

## Demo

A demo application is provided in the repository:

```bash
python demo_app.py
```

Then open your browser to http://localhost:8080.

## Complete Example

```python
from flask import Flask, render_template
from feedback import FeedbackSystem

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Create a feedback system instance
feedback_system = FeedbackSystem(
    exit_on_feedback=True    # Exit the app when receiving feedback
)

# Initialize the feedback system with the Flask app
feedback_system.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <h1 class="feedback-trigger">My Application</h1>
    <p>Right-click on the title to provide feedback!</p>
</body>
</html>
```
