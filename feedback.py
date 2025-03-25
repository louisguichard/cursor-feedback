from flask import Blueprint, request, jsonify
import os
import time


class FeedbackSystem:
    """
    A simple feedback system for Flask applications.

    This class provides a Flask blueprint with a route to handle feedback submissions
    and automatically injects the necessary JavaScript and CSS into your templates.
    """

    def __init__(
        self,
        exit_on_feedback=True,
    ):
        """
        Initialize the feedback system.

        Args:
            exit_on_feedback: Whether to exit the application after sending feedback
        """
        self.exit_on_feedback = exit_on_feedback
        self.app = None
        self.blueprint = None

    def init_app(self, app, enable_in_debug=True, enable_in_prod=False):
        """
        Initialize the feedback system with a Flask application.

        Args:
            app: The Flask application
            enable_in_debug: Whether to enable feedback in debug mode
            enable_in_prod: Whether to enable feedback in production mode
        """
        self.app = app

        # Create a Blueprint
        self.blueprint = Blueprint("feedback", __name__)

        # Add route to handle feedback
        @self.blueprint.route("/feedback", methods=["POST"])
        def handle_feedback():
            feedback_type = request.json.get("type")
            message = request.json.get("message", "")

            if feedback_type == "good":
                print("\n--- SUCCESS: User feedback is good! ---\n")
                if self.exit_on_feedback:
                    time.sleep(0.5)
                    os._exit(0)
                return jsonify(
                    {
                        "status": "success",
                        "message": "Thanks for the positive feedback!",
                    }
                )

            elif feedback_type == "issue":
                print(f"\n--- ERROR: User reported an issue: {message} ---\n")
                if self.exit_on_feedback:
                    time.sleep(0.5)
                    os._exit(1)
                return jsonify(
                    {"status": "success", "message": "Issue reported successfully!"}
                )

            return jsonify({"status": "error", "message": "Invalid feedback type"})

        # Register the blueprint
        app.register_blueprint(self.blueprint)

        # Determine if feedback is enabled
        @app.context_processor
        def inject_feedback_enabled():
            def is_feedback_enabled():
                return (app.debug and enable_in_debug) or (
                    not app.debug and enable_in_prod
                )

            return {"is_feedback_enabled": is_feedback_enabled}

        # Add after_request handler to inject the feedback script
        @app.after_request
        def inject_feedback_script(response):
            # Only inject in HTML responses when feedback is enabled
            if (
                response.content_type
                and response.content_type.startswith("text/html")
                and (
                    (app.debug and enable_in_debug)
                    or (not app.debug and enable_in_prod)
                )
            ):
                # The script to inject
                script = """
                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Create menu element
                    var feedbackMenu = document.createElement('div');
                    feedbackMenu.id = 'feedback-menu';
                    feedbackMenu.style.cssText = 'display: none; position: absolute; background-color: white; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); z-index: 1000; border-radius: 4px; overflow: hidden;';
                    
                    // Create menu items
                    var goodItem = document.createElement('div');
                    goodItem.textContent = 'Good';
                    goodItem.dataset.action = 'good';
                    goodItem.style.cssText = 'padding: 8px 12px;';
                    goodItem.addEventListener('mouseover', function() { this.style.backgroundColor = '#f0f0f0'; });
                    goodItem.addEventListener('mouseout', function() { this.style.backgroundColor = ''; });
                    
                    var issueItem = document.createElement('div');
                    issueItem.textContent = 'Report Issue';
                    issueItem.dataset.action = 'issue';
                    issueItem.style.cssText = 'padding: 8px 12px;';
                    issueItem.addEventListener('mouseover', function() { this.style.backgroundColor = '#f0f0f0'; });
                    issueItem.addEventListener('mouseout', function() { this.style.backgroundColor = ''; });
                    
                    // Add items to menu
                    feedbackMenu.appendChild(goodItem);
                    feedbackMenu.appendChild(issueItem);
                    
                    // Create modal element
                    var feedbackModal = document.createElement('div');
                    feedbackModal.id = 'feedback-modal';
                    feedbackModal.style.cssText = 'display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 1001; justify-content: center; align-items: center;';
                    
                    // Create modal content
                    var modalContent = document.createElement('div');
                    modalContent.style.cssText = 'background-color: white; padding: 20px; border-radius: 8px; width: 90%; max-width: 400px;';
                    
                    // Create modal title
                    var modalTitle = document.createElement('h3');
                    modalTitle.textContent = 'Report Issue';
                    modalTitle.style.cssText = 'margin-top: 0; margin-bottom: 15px;';
                    
                    // Create modal textarea
                    var feedbackMessage = document.createElement('textarea');
                    feedbackMessage.id = 'feedback-message';
                    feedbackMessage.placeholder = 'Describe the issue...';
                    feedbackMessage.style.cssText = 'width: 100%; min-height: 100px; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; font-family: inherit;';
                    
                    // Create modal buttons container
                    var modalButtons = document.createElement('div');
                    modalButtons.style.cssText = 'display: flex; justify-content: flex-end; gap: 10px;';
                    
                    // Create cancel button
                    var cancelButton = document.createElement('button');
                    cancelButton.textContent = 'Cancel';
                    cancelButton.id = 'cancel-feedback';
                    cancelButton.style.cssText = 'padding: 8px 16px; border: none; border-radius: 4px; background-color: #f0f0f0;';
                    
                    // Create submit button
                    var submitButton = document.createElement('button');
                    submitButton.textContent = 'Submit';
                    submitButton.id = 'submit-feedback';
                    submitButton.style.cssText = 'padding: 8px 16px; border: none; border-radius: 4px; background-color: #4CAF50; color: white;';
                    
                    // Add buttons to container
                    modalButtons.appendChild(cancelButton);
                    modalButtons.appendChild(submitButton);
                    
                    // Add everything to modal content
                    modalContent.appendChild(modalTitle);
                    modalContent.appendChild(feedbackMessage);
                    modalContent.appendChild(modalButtons);
                    
                    // Add content to modal
                    feedbackModal.appendChild(modalContent);
                    
                    // Add elements to document
                    document.body.appendChild(feedbackMenu);
                    document.body.appendChild(feedbackModal);
                    
                    // Add event listeners
                    document.querySelectorAll('.feedback-trigger').forEach(function(element) {
                        element.addEventListener('contextmenu', function(e) {
                            e.preventDefault();
                            
                            // Position the menu at the cursor
                            feedbackMenu.style.display = 'block';
                            feedbackMenu.style.left = e.pageX + 'px';
                            feedbackMenu.style.top = e.pageY + 'px';
                        });
                    });
                    
                    // Hide menu when clicking elsewhere
                    document.addEventListener('click', function() {
                        feedbackMenu.style.display = 'none';
                    });
                    
                    // Handle menu item clicks
                    goodItem.addEventListener('click', function() {
                        sendFeedback('good');
                    });
                    
                    issueItem.addEventListener('click', function() {
                        feedbackModal.style.display = 'flex';
                    });
                    
                    // Handle modal buttons
                    cancelButton.addEventListener('click', function() {
                        feedbackModal.style.display = 'none';
                        feedbackMessage.value = '';
                    });
                    
                    submitButton.addEventListener('click', function() {
                        var message = feedbackMessage.value.trim();
                        if (message) {
                            sendFeedback('issue', message);
                            feedbackModal.style.display = 'none';
                            feedbackMessage.value = '';
                        } else {
                            alert('Please describe the issue.');
                        }
                    });
                    
                    // Send feedback to server
                    function sendFeedback(type, message) {
                        fetch('/feedback', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ type: type, message: message || '' }),
                        })
                        .then(function(response) { return response.json(); })
                        .then(function(data) {
                            if (data.status === 'success') {
                                alert('Feedback sent: ' + data.message);
                            } else {
                                alert('Error: ' + data.message);
                            }
                        })
                        .catch(function(error) {
                            console.error('Error sending feedback:', error);
                        });
                    }
                });
                </script>
                """

                # Inject script before the closing </body> tag
                response.data = response.data.replace(
                    b"</body>", f"{script}</body>".encode()
                )

            return response
