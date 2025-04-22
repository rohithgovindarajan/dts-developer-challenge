# src/main/python/uk/gov/hmcts/reform/dev/schemas.py

from marshmallow import Schema, fields, ValidationError, validates
from datetime import datetime

# Define a set of valid statuses for the task
VALID_STATUSES = {'pending', 'in-progress', 'done'}

class TaskSchema(Schema):
    # Field for task ID, only included in serialized output
    id = fields.Int(dump_only=True)
    
    # Field for task title, required and must be non-empty
    title = fields.Str(required=True, validate=lambda s: len(s) > 0)
    
    # Field for task description, optional with a default value of an empty string
    description = fields.Str(load_default='')  # ← use load_default
    
    # Field for task status, required and must be validated
    status = fields.Str(required=True)
    
    # Field for task due date, optional and can be None
    due = fields.DateTime(allow_none=True)
    
    # Field for task creation timestamp, only included in serialized output
    created_at = fields.DateTime(dump_only=True)

    # Custom validator for the 'status' field
    @validates('status')
    def check_status(self, v):
        # Raise a validation error if the status is not in the valid set
        if v not in VALID_STATUSES:
            raise ValidationError(f"Status must be one of {VALID_STATUSES}")
