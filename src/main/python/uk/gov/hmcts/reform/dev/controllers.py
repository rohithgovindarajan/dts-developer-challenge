# src/main/python/uk/gov/hmcts/reform/dev/controllers.py

from flask import Blueprint, request, jsonify, abort
from datetime import datetime

from uk.gov.hmcts.reform.dev.Application import basic_auth, db
from uk.gov.hmcts.reform.dev.models import Task, VALID_STATUSES

# Define a Blueprint for task-related routes
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# CORS preflight handler for all task-related routes
@tasks_bp.route('', methods=['OPTIONS'])
@tasks_bp.route('/<int:id>', methods=['OPTIONS'])
@tasks_bp.route('/<int:id>/status', methods=['OPTIONS'])
def options_all(id=None):
    # Return a 204 No Content response for preflight requests
    return '', 204

# List all tasks
@tasks_bp.route('', methods=['GET'])
@basic_auth.required
def list_tasks():
    # Retrieve all tasks from the database and return them as JSON
    return jsonify([t.to_dict() for t in Task.query.all()]), 200

# Create a new task
@tasks_bp.route('', methods=['POST'])
@basic_auth.required
def create_task():
    # Parse JSON data from the request
    data = request.get_json(force=True) or {}
    title = data.get('title')
    status = data.get('status')

    # Validate the 'title' field
    if not title or not isinstance(title, str):
        abort(400, description="Missing or invalid 'title'")
    # Validate the 'status' field
    if status not in VALID_STATUSES:
        abort(400, description=f"Invalid 'status'; must be one of {VALID_STATUSES}")

    # Parse and validate the 'due' field if provided
    due = None
    if data.get('due'):
        try:
            due = datetime.fromisoformat(data['due'])
        except:
            abort(400, description="Invalid 'due'; use ISO8601")

    # Create a new Task object and save it to the database
    task = Task(
        title=title,
        description=data.get('description', ''),
        status=status,
        due=due
    )
    db.session.add(task)
    db.session.commit()
    # Return the created task as JSON with a 201 Created status
    return jsonify(task.to_dict()), 201

# Retrieve a single task by its ID
@tasks_bp.route('/<int:id>', methods=['GET'])
@basic_auth.required
def get_task(id):
    # Fetch the task from the database or return a 404 error if not found
    task = Task.query.get_or_404(id)
    # Return the task as JSON
    return jsonify(task.to_dict()), 200

# Update only the status of a task
@tasks_bp.route('/<int:id>/status', methods=['PATCH'])
@basic_auth.required
def update_status(id):
    # Fetch the task from the database or return a 404 error if not found
    task = Task.query.get_or_404(id)
    # Parse JSON data from the request
    data = request.get_json(force=True) or {}

    # Validate the 'status' field
    new_status = data.get('status')
    if not new_status:
        abort(400, description="Missing 'status' field")
    if new_status not in VALID_STATUSES:
        abort(400, description=f"Invalid 'status'; must be one of {VALID_STATUSES}")

    # Update the task's status and save the changes to the database
    task.status = new_status
    db.session.commit()
    # Return the updated task as JSON
    return jsonify(task.to_dict()), 200

# Delete a task by its ID
@tasks_bp.route('/<int:id>', methods=['DELETE'])
@basic_auth.required
def delete_task(id):
    # Fetch the task from the database or return a 404 error if not found
    task = Task.query.get_or_404(id)
    # Delete the task from the database
    db.session.delete(task)
    db.session.commit()
    # Return a 204 No Content response
    return '', 204
