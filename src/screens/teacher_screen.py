import streamlit as st
import html as py_html

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    DatabaseConnectionError,
    get_attendance_for_teacher,
    get_enrolled_students_for_subject,
    get_teacher_subjects,
    teacher_login,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np # img to numpy array

from datetime import datetime # attendance timestamp

import pandas as pd

from src.components.dialog_voice_attendance import voice_attendance_dialog


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

# if teacher already logged in
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([2.0,1], vertical_alignment='center', gap='medium')

    with c1:
        # dashboard title
        st.markdown("""
        <h1 style='
            font-size:2.45rem;
            line-height:1.05;
            font-weight:700;
            color:#A78BFA;
            margin-bottom:0.2rem;
        '>
        Teacher Dashboard
        </h1>
        """, unsafe_allow_html=True)

        # subtitle
        st.markdown("""
        <p style='
            color:#9CA3AF;
            margin-bottom:1.2rem;
        '>
        Manage attendance using AI-powered automation.
        </p>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
        # welcome text
        st.markdown(
            f"""
            <h2 style='
                text-align:right;
                font-size:1.65rem;
                margin-bottom:0.6rem;
            '>
                Welcome, {teacher_data['name']}
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
        # logout button
        if st.button("Logout", type='secondary', key='loginbackbtn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()
            st.caption("Shortcut: Ctrl + Backspace")

# default tab
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3, gap='medium')


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.markdown("""
        <div style="
            height:1px;
            background:rgba(255,255,255,0.06);
            margin-top:1.4rem;
            margin-bottom:1.4rem;
        "></div>
        """, unsafe_allow_html=True)


    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
   

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    try:
        subjects = get_teacher_subjects(teacher_id)
    except DatabaseConnectionError as exc:
        st.error(str(exc))
        return

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    st.markdown(
        """
        <style>
            .st-key-take-attendance-controls{
                border:1px solid rgba(196,181,253,0.17);
                border-radius:16px;
                padding:14px 14px 8px 14px;
                background:
                    radial-gradient(circle at 10% 10%, rgba(167,139,250,0.10), transparent 35%),
                    linear-gradient(145deg, rgba(12,12,25,0.86), rgba(8,8,20,0.92));
                box-shadow:
                    0 10px 24px rgba(0,0,0,0.30),
                    0 0 0 1px rgba(139,92,246,0.10) inset;
                margin-bottom:12px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=False, key="take-attendance-controls"):
        col1, col2 = st.columns([4,1.3], vertical_alignment='bottom')

        with col1:
            selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

        with col2:
            if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
                st.session_state.show_photo_dialog = True

    if st.session_state.get("show_photo_dialog", False):
        add_photos_dialog()
        
    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

    
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
        has_photos = bool(st.session_state.attendance_images)
        c1, c2, c3 = st.columns(3)


        with c1:
            if st.button(
                'Clear all photos',
                width='stretch',
                type='tertiary',
                icon=':material/delete:',
                disabled=not has_photos
            ):
                st.session_state.attendance_images = []
                st.rerun()


        with c2:

            if st.button(
                'Run Face Analysis',
                width='stretch',
                type='secondary',
                icon=':material/analytics:',
                disabled=not has_photos
            ):

            # shows loading animation
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_ids = {}

                    for idx, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB')) # PIL img --> numpy RGB array
                        try:
                            detected, _, _ = predict_attendance(img_np)
                        except DatabaseConnectionError as exc:
                            st.error(str(exc))
                            return

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                    try:
                        enrolled_students = get_enrolled_students_for_subject(selected_subject_id)
                    except DatabaseConnectionError as exc:
                        st.error(str(exc))
                        return

                    if not enrolled_students:
                        st.warning('No students enrolled in this course')

                    else:

                        results, attendance_to_log = [], []

                        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                        for node in enrolled_students:

                            student = node['students']

                            sources = all_detected_ids.get(
                                int(student['student_id']),
                                []
                            )

                            is_present = len(sources) > 0

                            results.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "-",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        attendance_result_dialog(
                            pd.DataFrame(results),
                            attendance_to_log
                        )


        with c3:
            if st.button(
                'Use Voice Attendance',
                type='primary',
                width='stretch',
                icon=':material/mic:'
            ):
                voice_attendance_dialog(selected_subject_id)



def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    try:
        subjects = get_teacher_subjects(teacher_id)
    except DatabaseConnectionError as exc:
        st.error(str(exc))
        return
    if subjects:
        for sub in subjects:

            stats = [
                ("🫂", "Students", sub['total_students']),
                ("📚", "Classes", sub['total_classes']),
            ]

            
            def share_button():
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:",
                    width='stretch'
                ):
                    share_subject_dialog(
                        sub['name'],
                        sub['subject_code']
                    )

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_button,
            )

            st.space()
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def _teacher_tab_attendance_records_legacy():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    try:
        records = get_attendance_for_teacher(teacher_id)
    except DatabaseConnectionError as exc:
        st.error(str(exc))
        return

    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            # convert timestamp string to datetime object
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.table(display_df)


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False)),
        })

    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + " Students"
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance Stats', 'Present_Count', 'Total_Count']]
    )

    rows_html = []
    for _, row in display_df.iterrows():
        time_val = py_html.escape(str(row['Time']))
        subject_val = py_html.escape(str(row['Subject']))
        code_val = py_html.escape(str(row['Subject Code']))
        stats_text = py_html.escape(str(row['Attendance Stats']))
        present_count = int(row['Present_Count'])
        total_count = int(row['Total_Count'])
        badge_bg = "rgba(16,185,129,0.18)" if present_count == total_count else "rgba(251,191,36,0.18)"
        badge_fg = "#A7F3D0" if present_count == total_count else "#FDE68A"

        rows_html.append(
            "<tr>"
            f"<td class='col-time'>{time_val}</td>"
            f"<td class='col-subject'>{subject_val}</td>"
            f"<td class='col-code'>{code_val}</td>"
            "<td class='col-stats'>"
            f"<span class='attendance-badge' style='background:{badge_bg};color:{badge_fg};'>{stats_text}</span>"
            "</td>"
            "</tr>"
        )

    table_html = (
        "<style>"
        ".attendance-table-wrap{border:1px solid rgba(196,181,253,0.18);border-radius:18px;overflow:hidden;"
        "background:"
        "radial-gradient(circle at 12% 18%, rgba(168,85,247,0.10), transparent 40%),"
        "linear-gradient(145deg, rgba(12,12,26,0.90), rgba(8,8,20,0.95));"
        "box-shadow:0 14px 32px rgba(0,0,0,0.38),0 0 0 1px rgba(139,92,246,0.15) inset;"
        "backdrop-filter:blur(14px);} "
        ".attendance-table{width:100%;border-collapse:collapse;font-size:0.98rem;} "
        ".attendance-table thead th{text-align:left;padding:14px 16px;color:#EEE9FF;"
        "background:linear-gradient(135deg, rgba(147,51,234,0.34), rgba(124,58,237,0.24));"
        "border-bottom:1px solid rgba(221,214,254,0.22);font-weight:700;letter-spacing:0.2px;} "
        ".attendance-table tbody td{padding:13px 16px;color:#F5F3FF;border-bottom:1px solid rgba(196,181,253,0.09);} "
        ".attendance-table tbody tr:nth-child(even){background:rgba(139,92,246,0.08);} "
        ".attendance-table tbody tr:nth-child(odd){background:rgba(255,255,255,0.025);} "
        ".attendance-table tbody tr:hover{background:rgba(139,92,246,0.16);} "
        ".attendance-table .col-time{color:#D6CCFF;font-weight:500;} "
        ".attendance-table .col-subject{color:#F3EEFF;font-weight:600;} "
        ".attendance-table .col-code{color:#D6CCFF;letter-spacing:0.3px;} "
        ".attendance-table .col-stats{text-align:left;} "
        ".attendance-badge{display:inline-block;border-radius:999px;padding:4px 10px;font-weight:700;font-size:0.9rem;"
        "border:1px solid rgba(255,255,255,0.18);}"
        "</style>"
        "<div class='attendance-table-wrap'>"
        "<table class='attendance-table'>"
        "<thead><tr><th>Time</th><th>Subject</th><th>Subject Code</th><th>Attendance Stats</th></tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    
    try:
        teacher = teacher_login(username, password)
    except DatabaseConnectionError as exc:
        st.error(str(exc))
        return False

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    

    return False


def teacher_screen_login():
    header_dashboard()

    st.markdown("""
    <p style='
        color:#9CA3AF;
        text-align:center;
        margin-top:-8px;
        margin-bottom:2rem;
        font-size:1rem;
    '>
        Manage attendance using AI-powered automation.
    </p>
    """, unsafe_allow_html=True)
    st.space()
    c1, c2, c3 = st.columns([2,2,2])

    with c2:
        if st.button("← Go back to Home", type='secondary', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
    <h2 style="
        text-align:center;
        font-size:1.85rem;
        margin-bottom:1.3rem;
        color:#F3EEFF;
    ">
        Login Using Password
    </h2>
    """, unsafe_allow_html=True)
    st.space()

    left, center, right = st.columns([0.7,4,0.7])
    
    with center:
        teacher_username = st.text_input("Enter username", placeholder='E.g: tanmayee26')

        teacher_pass = st.text_input("Enter password", type='password', placeholder="E.g: tanu@123")

        st.divider()

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Login', icon=':material/passkey:', width='stretch'):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("welcome back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                    st.caption("Shortcut: Ctrl + Enter")

                else:
                    st.error("Invalid username and password combo")

        with btnc2:
            if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
                st.session_state.teacher_login_type = 'register'


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    try:
        if check_teacher_exists(teacher_username):
            return False, "Username already taken"
    except DatabaseConnectionError as exc:
        return False, str(exc)
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except DatabaseConnectionError as exc:
        return False, str(exc)
    except Exception:
        return False, "Unexpected Error!"
    

def teacher_screen_register():
    header_dashboard()
    st.space()
    c1, c2, c3 = st.columns([2,2,2])

    with c2:
        if st.button("← Go back to Home", type='secondary', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()


    st.markdown("""
    <p style='
        color:#9CA3AF;
        text-align:center;
        margin-top:-8px;
        margin-bottom:2rem;
        font-size:1rem;
    '>
        Manage attendance using AI-powered automation.
    </p>
    """, unsafe_allow_html=True)
    

    st.markdown("""
    <h2 style="
        text-align:center;
        font-size:1.85rem;
        margin-bottom:1.3rem;
        color:#F3EEFF;
    ">
        Register Your Teacher Profile
    </h2>
    """, unsafe_allow_html=True)

    st.space()

    left, center, right = st.columns([0.7,4,0.7])
        
    with center:

        teacher_username = st.text_input(
            "Enter username",
            placeholder='E.g: tanmayee26'
        )

        teacher_name = st.text_input(
            "Enter name",
            placeholder='Tanmayee Satpathy'
        )

        teacher_pass = st.text_input(
            "Enter password",
            type='password',
            placeholder="E.g: tanu@123"
        )

        teacher_pass_confirm = st.text_input(
            "Confirm your password",
            type='password',
            placeholder="E.g: tanu@123"
        )

    with center:

        st.markdown("""
        <hr style="
            border:0;
            height:1px;
            background:rgba(255,255,255,0.08);
            margin-top:2rem;
            margin-bottom:2rem;
        ">
        """, unsafe_allow_html=True)


    with center:

        btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
                st.caption("Shortcut: Ctrl + Enter")
            else:
                st.error(message)


    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'
