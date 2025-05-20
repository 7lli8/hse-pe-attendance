from sqlalchemy import select
from sqlalchemy.orm import Session

from enums import AttestationType

from .models import AttendanceRequirement


def get_requirements_visits(session: Session) -> dict[AttestationType, int]:
    requirements_dict = {}
    requirements = list(session.scalars(select(AttendanceRequirement)).all())
    for requirement in requirements:
        requirements_dict[requirement.attestation_type] = requirement.required_visits
    return requirements_dict
