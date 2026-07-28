from src.database.config import supabase
import bcrypt # password hashing library
import httpx
import logging

try:
    from postgrest.exceptions import APIError as PostgrestAPIError
except ImportError:  # pragma: no cover - depends on supabase package version
    PostgrestAPIError = ()


logger = logging.getLogger(__name__)


class DatabaseConnectionError(RuntimeError):
    """Raised when Supabase cannot be reached from the app runtime."""


def _execute(request):
    try:
        return request.execute()
    except PostgrestAPIError as exc:
        logger.exception("Supabase API request failed")
        raise DatabaseConnectionError(_friendly_api_error_message(exc)) from exc
    except httpx.HTTPError as exc:
        logger.exception("Supabase HTTP request failed")
        raise DatabaseConnectionError(
            "Could not connect to the database. Please check your internet connection "
            "and Supabase settings, then try again."
        ) from exc


def _friendly_api_error_message(exc):
    error_text = str(exc).lower()

    if "jwt" in error_text or "api key" in error_text or "unauthorized" in error_text:
        return (
            "Database authentication failed. Please check your Supabase URL and API key "
            "in Streamlit secrets."
        )

    if "relation" in error_text and "does not exist" in error_text:
        return (
            "A required database table is missing. Please confirm your Supabase schema "
            "contains teachers, students, subjects, subject_students, and attendance_logs."
        )

    if "permission denied" in error_text or "row-level security" in error_text or "rls" in error_text:
        return (
            "The database blocked this request. Please check your Supabase row-level "
            "security policies for this table."
        )

    return (
        "The database rejected this request. Please check your Supabase schema, "
        "table policies, and Streamlit secrets."
    )


def hash_pass(pwd):
    # encode string to bytes , generate random salt , convert bytes to string
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()


def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())


def check_teacher_exists(username):
    response = _execute(supabase.table("teachers").select("username").eq("username",username))
    return len(response.data) > 0


def create_teacher(username,password,name):
    data = {"username" : username, "password":hash_pass(password),"name":name}
    response = _execute(supabase.table("teachers").insert(data))
    return response.data

def teacher_login(username,password):
    response = _execute(supabase.table("teachers").select("*").eq("username",username))
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None    


def get_all_students():
    response = _execute(supabase.table('students').select("*"))
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name':new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
    response = _execute(supabase.table("students").insert(data))
    return response.data

def create_subject(subject_code,name,section,teacher_id):
    data = {"subject_code":subject_code,"name":name,"section":section,"teacher_id":teacher_id}
    response = _execute(supabase.table("subjects").insert(data))
    return response.data

def get_teacher_subjects(teacher_id):
    response = _execute(supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id))
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects

def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= _execute(supabase.table('subject_students').insert(data))
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= _execute(supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id))
    return response.data

def get_student_subjects(student_id):
    response = _execute(supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id))
    return response.data


def get_subject_by_code(subject_code):
    response = _execute(
        supabase.table('subjects')
        .select('subject_id, name, subject_code')
        .eq('subject_code', subject_code)
    )
    return response.data[0] if response.data else None


def is_student_enrolled(student_id, subject_id):
    response = _execute(
        supabase.table('subject_students')
        .select('*')
        .eq('subject_id', subject_id)
        .eq('student_id', student_id)
    )
    return bool(response.data)


def get_enrolled_students_for_subject(subject_id):
    response = _execute(
        supabase.table('subject_students')
        .select("*, students(*)")
        .eq('subject_id', subject_id)
    )
    return response.data


def get_student_attendance(student_id):
    response = _execute(supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id))
    return response.data

def create_attendance(logs):
    response = _execute(supabase.table('attendance_logs').insert(logs))
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = _execute(supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id))
    return response.data
