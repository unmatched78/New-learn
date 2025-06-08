# core/tasks.py

from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    """
    Simple example task: returns x + y.
    You can call add.delay(4, 5) from anywhere.
    """
    return x + y

@shared_task
def mark_note_as_old(note_id):
    """
    Example: print a log with the note ID and timestamp.
    In a real app, you might archive or notify.
    """
    from .models import Note

    try:
        note = Note.objects.get(id=note_id)
        # (Just logging for demonstration)
        logger.info(f"Note {note_id} marked as old at {timezone.now()}")
        return f"Marked note {note_id}"
    except Note.DoesNotExist:
        return f"Note {note_id} not found"
