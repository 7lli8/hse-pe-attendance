import io

from openpyxl import Workbook

from enums import AttestationType

from .models import Student


def get_attestation_verdict(total_visits: int, required_visits: dict) -> str:
    print(required_visits)
    if total_visits >= required_visits.get(AttestationType.AUTO_CREDIT, 0):
        return "автомат"
    elif total_visits >= required_visits.get(AttestationType.CREDIT, 0):
        return "зачёт"
    else:
        return "незачёт"


def get_attestation_progress(
    total_visits: int, required_visits: dict[AttestationType, int]
) -> dict[str, dict]:
    result = {}
    for enum_key, alias, color in [
        (AttestationType.CREDIT, "credit", None),
        (AttestationType.AUTO_CREDIT, "auto", None),
    ]:
        required = required_visits.get(enum_key, 0)
        current = min(total_visits, required)
        result[alias] = {
            "current": current,
            "required": required,
            "remaining": max(0, required - current),
        }
    return result


def generate_attendance_xlsx(students: list[Student], required_visits: dict) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Ведомость"

    ws.append(
        [
            "№",
            "Фамилия",
            "Имя",
            "Отчество",
            "Курс",
            "Группа",
            "Количество посещений",
            "Вердикт",
        ]
    )

    students_sorted = sorted(
        students, key=lambda s: (s.group.name if s.group else "", s.last_name)
    )

    for i, student in enumerate(students_sorted, start=1):
        full_visits = student.total_attendances
        verdict = get_attestation_verdict(full_visits, required_visits)

        ws.append(
            [
                i,
                student.last_name,
                student.first_name,
                student.middle_name,
                student.course,
                student.group.name if student.group else "-",
                full_visits,
                verdict,
            ]
        )

    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
