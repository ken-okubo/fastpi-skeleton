from datetime import datetime, timezone
from typing import Annotated

from pydantic import PlainSerializer


def serialize_datetime(dt: datetime) -> str:
    """Custom datetime serializer that outputs UTC with Z suffix."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


DateTimeUTC = Annotated[datetime, PlainSerializer(serialize_datetime)]
