from sqlalchemy import select
from sqlalchemy.orm import Session

from enums import AttestationType

from .models import AttendanceRequirement


def save_attestation(session: Session, credit: int, automat: int):
    for attestation_type, visits in [
        (AttestationType.CREDIT, credit),
        (AttestationType.AUTO_CREDIT, automat),
    ]:
        requirement = AttendanceRequirement(
            attestation_type=attestation_type,
            required_visits=visits,
        )
        if obj := session.execute(
            select(AttendanceRequirement).where(
                AttendanceRequirement.attestation_type == attestation_type
            )
        ).scalar_one_or_none():
            requirement = obj

        requirement.required_visits = visits
        session.add(requirement)
    session.commit()
