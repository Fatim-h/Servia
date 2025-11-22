from app.models import Cause
from sqlalchemy import func
from app import db

def get_next_cause_id(cause_type):
    """
    Returns the next cause_id for a new cause.
    NGO: even IDs, Event: odd IDs
    """
    if cause_type.lower() == "ngo":
        max_even = db.session.query(func.max(Cause.cause_id)).filter(Cause.cause_id % 2 == 0).scalar()
        return (max_even or 0) + 2
    elif cause_type.lower() == "event":
        max_odd = db.session.query(func.max(Cause.cause_id)).filter(Cause.cause_id % 2 == 1).scalar()
        return (max_odd or -1) + 2
    else:
        raise ValueError("Invalid cause type")