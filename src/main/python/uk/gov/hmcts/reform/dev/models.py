# src/main/python/uk/gov/hmcts/reform/dev/models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from uk.gov.hmcts.reform.dev.Application import db

VALID_STATUSES = {'pending', 'in progress', 'done'}

class Task(db.Model):
    """
    Task Model
    Represents a task entity in the database.
    Attributes:
        id (int): The primary key for the task.
        title (str): The title of the task, limited to 200 characters. Cannot be null.
        description (str): A detailed description of the task. Can be null.
        status (Enum): The current status of the task. Must be one of the valid statuses defined in VALID_STATUSES.
        due (datetime): The due date and time for the task. Can be null.
        created_at (datetime): The timestamp when the task was created. Defaults to the current UTC time.
    Methods:
        to_dict():
            Converts the Task object into a dictionary representation.
            Returns:
                dict: A dictionary containing the task's attributes in a serializable format.
    """
    __tablename__ = 'tasks'

    id          = Column(Integer, primary_key=True)
    title       = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(Enum(*VALID_STATUSES, name='status'), nullable=False)
    due         = Column(DateTime, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description,
            'status':      self.status,
            'due':         self.due.isoformat() if self.due else None,
            'created_at':  self.created_at.isoformat(),
        }
