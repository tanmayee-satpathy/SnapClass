
from src.database.config import supabase
import bcrypt
import httpx
import logging

try:
    from postgrest.exceptions import APIError as PostgrestAPIError
except ImportError:
    PostgrestAPIError = ()


logger = logging.getLogger(__name__)


class DatabaseConnectionError(RuntimeError):
    """Raised when Supabase cannot be reached from the app runtime."""


def _execute(request):
    """Execute a Supabase request and log the underlying error."""
    try:
        return request.execute()

    except PostgrestAPIError as exc:
        # Diagnostic logging: inspect Streamlit Cloud logs for this message.
        logger.exception("SUPABASE API ERROR: %r", exc)
        raise DatabaseConnectionError(
            _friendly_api_error_message(exc)
        ) from exc

    except httpx.HTTPError as exc:
        logger.exception("SUPABASE HTTP ERROR: %r", exc)
        raise DatabaseConnectionError(
            "Could not connect to Supabase. Check the project URL, "
            "API key, network connection, and project status."
        ) from exc

    except Exception as exc:
        # Keep unexpected errors visible in the logs.
        logger.exception("UNEXPECTED DATABASE ERROR: %r", exc)
        raise DatabaseConnectionError(
            "An unexpected database error occurred. "
            "Check the Streamlit Cloud logs."
        ) from exc


def _friendly_api_error_message(exc):
    error_text = str(exc).lower()

    if any(term in error_text for term in (
        "jwt", "api key", "unauthorized", "invalid api key"
    )):
        return (
            "Database authentication failed. Check the Supabase URL "
            "and API key in Streamlit Cloud Secrets."
        )

    if "does not exist" in error_text and (
        "relation" in error_text or "column" in error_text
    ):
        return (
            "A required database table or column is missing. "
            "Check the SnapClass database schema."
        )

    if "null value" in error_text and "not-null constraint" in error_text:
        return (
            "Supabase rejected a blank value for a required column. "
            "Check that auto-generated ID columns are configured correctly."
        )

    if any(term in error_text for term in (
        "permission denied", "row-level security",
        "violates row-level security policy", "rls"
    )):
        return (
            "Supabase blocked the database request. "
            "Check table permissions and Row Level Security policies."
        )

    return (
        "Supabase rejected the database request. "
        "Check the detailed application logs."
    )


def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )


def check_teacher_exists(username):
    response = _execute(
        supabase.table("teachers")
        .select("username")
        .eq("username", username)
    )
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = _execute(
        supabase.table("teachers").insert(data)
    )
    return response.data


def teacher_login(username, password):
    response = _execute(
        supabase.table("teachers")
        .select("*")
        .eq("username", username)
    )

    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher

    return None


def get_all_students():
    response = _execute(
        supabase.table("students").select("*")
    )
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }

    response = _execute(
        supabase.table("students").insert(data)
    )
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id,
    }
    response = _execute(
        supabase.table("subjects").insert(data)
    )
    return response.data


def get_teacher_subjects(teacher_id):
    response = _execute(
        supabase.table("subjects")
        .select(
            "*, subject_students(count), attendance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
    )

    subjects = response.data

    for sub in subjects:
        enrollment = sub.get("subject_students") or []
        sub["total_students"] = (
            enrollment[0].get("count", 0) if enrollment else 0
        )

        attendance = sub.get("attendance_logs") or []
        sub["total_classes"] = len({
            log["timestamp"]
            for log in attendance
            if log.get("timestamp") is not None
        })

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id,
    }
    response = _execute(
        supabase.table("subject_students").insert(data)
    )
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = _execute(
        supabase.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
    )
    return response.data


def get_student_subjects(student_id):
    response = _execute(
        supabase.table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
    )
    return response.data


def get_subject_by_code(subject_code):
    response = _execute(
        supabase.table("subjects")
        .select("subject_id, name, subject_code")
        .eq("subject_code", subject_code)
    )
    return response.data[0] if response.data else None


def is_student_enrolled(student_id, subject_id):
    response = _execute(
        supabase.table("subject_students")
        .select("*")
        .eq("subject_id", subject_id)
        .eq("student_id", student_id)
    )
    return bool(response.data)


def get_enrolled_students_for_subject(subject_id):
    response = _execute(
        supabase.table("subject_students")
        .select("*, students(*)")
        .eq("subject_id", subject_id)
    )
    return response.data


def get_student_attendance(student_id):
    response = _execute(
        supabase.table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
    )
    return response.data


def create_attendance(logs):
    response = _execute(
        supabase.table("attendance_logs").insert(logs)
    )
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = _execute(
        supabase.table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
    )
    return response.data
