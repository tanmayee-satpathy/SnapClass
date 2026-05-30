import html as py_html
import time

import numpy as np
import streamlit as st
from PIL import Image

from src.components.dialog_enroll import enroll_dialog
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    create_student,
    get_all_students,
    get_student_attendance,
    get_student_subjects,
    unenroll_student_to_subject,
)
from src.pipelines.face_pipeline import (
    get_face_embeddings,
    predict_attendance,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_background_dashboard, style_base_layout


def _inject_student_ui_styles():
    st.markdown(
        """
        <style>
            .student-subtitle{
                color:#B8B2CC;
                margin-top:0.1rem;
                margin-bottom:0.9rem;
                font-size:1.02rem;
            }

            .student-subtitle-center{
                text-align:center;
                color:#d8d6e8;
                margin-top:0.15rem;
                margin-bottom:0.55rem;
                font-size:0.98rem;
            }

            .student-divider{
                height:1px;
                background:rgba(255,255,255,0.08);
                margin-top:0.8rem;
                margin-bottom:1rem;
            }

            .student-welcome{
                text-align:right;
                color:#F3EEFF;
                font-size:1.32rem;
                font-weight:700;
                margin-top:0.2rem;
                margin-bottom:0.5rem;
            }

            .student-section-title{
                text-align:left;
                color:#F5F3FF;
                font-size:1.75rem;
                font-weight:700;
                margin:0 0 0.35rem 0;
            }

            .st-key-student-face-shell{
                border:1px solid rgba(196,181,253,0.22);
                border-radius:16px;
                padding:12px 12px 6px 12px;
                background:
                    radial-gradient(circle at 14% 10%, rgba(167,139,250,0.10), transparent 36%),
                    linear-gradient(145deg, rgba(12,12,25,0.88), rgba(8,8,20,0.94));
                box-shadow:
                    0 12px 28px rgba(0,0,0,0.34),
                    0 0 0 1px rgba(139,92,246,0.12) inset;
            }

            .st-key-student-face-shell [data-testid="stCameraInput"] > div{
                border-radius:12px !important;
                overflow:hidden !important;
                border:1px solid rgba(196,181,253,0.18) !important;
            }

            .st-key-student-register-shell{
                border:1px solid rgba(196,181,253,0.20);
                border-radius:16px;
                padding:12px 14px 10px 14px;
                background:
                    radial-gradient(circle at 10% 14%, rgba(167,139,250,0.08), transparent 36%),
                    linear-gradient(145deg, rgba(13,13,28,0.88), rgba(9,9,22,0.93));
                box-shadow:
                    0 10px 22px rgba(0,0,0,0.30),
                    0 0 0 1px rgba(139,92,246,0.10) inset;
            }

            .student-register-note{
                color:#C4B5FD;
                font-size:0.92rem;
                margin-top:0.2rem;
                margin-bottom:0.6rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def student_dashboard():
    _inject_student_ui_styles()

    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    c1, c2 = st.columns([2.1, 1], vertical_alignment="center", gap="medium")
    with c1:
        header_dashboard("Student Dashboard")
        st.markdown(
            "<p class='student-subtitle'>Track your classes and attendance at a glance.</p>",
            unsafe_allow_html=True,
        )
    with c2:
        safe_name = py_html.escape(str(student_data["name"]))
        st.markdown(
            f"<div class='student-welcome'>Welcome, {safe_name}</div>",
            unsafe_allow_html=True,
        )
        if st.button("Logout", type="secondary", key="student_logout_btn"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()

    st.markdown("<div class='student-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1], gap="medium")
    with c1:
        st.markdown(
            "<h2 class='student-section-title'>Your Enrolled Subjects</h2>",
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
            enroll_dialog()

    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    if not subjects:
        st.info("You are not enrolled in any subject yet. Use the button above to join one.")
        footer_dashboard()
        return

    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    cols = st.columns(2, gap="medium")
    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button():
            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                icon=":material/delete_forever:",
                key=f"unenroll_{sid}",
            ):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("", "Total Classes", stats["total"]),
                    ("", "Attended", stats["attended"]),
                ],
                footer_callback=unenroll_button,
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()
    _inject_student_ui_styles()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns([2.1, 1], vertical_alignment="center", gap="medium")
    with c1:
        header_dashboard("Student Dashboard")
    with c2:
        if st.button("Go back to Home", type="secondary", key="student_back_home_btn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div class='student-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='student-subtitle-center'>Quick secure access with FaceID.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align:center;margin-bottom:0.6rem;'>Login Using FaceID</h2>",
        unsafe_allow_html=True,
    )

    show_registration = False

    left, center, right = st.columns([0.7, 4, 0.7])
    with center:
        with st.container(border=False, key="student-face-shell"):
            photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning..."):
            detected, _, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found.")
            elif num_faces > 1:
                st.warning("Multiple faces found. Please keep only one face in frame.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s["student_id"] == student_id),
                        None,
                    )
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    show_registration = True

    if show_registration:
        with center:
            with st.container(border=False, key="student-register-shell"):
                st.header("Create Student Profile")
                st.markdown(
                    "<p class='student-register-note'>Face not recognized. Create your profile below.</p>",
                    unsafe_allow_html=True,
                )
                new_name = st.text_input(
                    "Enter your name",
                    placeholder="E.g. Tanmayee",
                    key="student_register_name",
                )
                st.subheader("Optional Voice Enrollment")
                st.caption("Voice enrollment can take extra time on first use.")

                enable_voice_now = st.checkbox(
                    "Add voice profile now (slower)",
                    value=False,
                    key="student_enable_voice_now",
                )

                audio_data = None
                if enable_voice_now:
                    try:
                        audio_data = st.audio_input(
                            "Record a short phrase like: I am present, my name is Akash.",
                            key="student_register_audio",
                        )
                    except Exception:
                        st.error("Audio input is not available.")

                if st.button(
                    "Create Account",
                    type="primary",
                    width="stretch",
                    key="student_create_account_btn",
                ):
                    if new_name:
                        with st.spinner("Creating profile..."):
                            img = np.array(Image.open(photo_source))
                            encodings = get_face_embeddings(img)
                            if encodings:
                                face_emb = encodings[0].tolist()
                                voice_emb = None
                                if enable_voice_now and audio_data:
                                    voice_emb = get_voice_embedding(audio_data.read())

                                response_data = create_student(
                                    new_name,
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb,
                                )

                                if response_data:
                                    # Skip synchronous model retraining here to keep signup fast.
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = response_data[0]
                                    st.toast(f"Profile created. Hi {new_name}!")
                                    st.rerun()
                            else:
                                st.error("Could not capture facial features for registration.")
                    else:
                        st.warning("Please enter your name.")

    footer_dashboard()
