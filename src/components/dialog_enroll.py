import streamlit as st
from src.database.db import (
    DatabaseConnectionError,
    enroll_student_to_subject,
    get_subject_by_code,
    is_student_enrolled,
)
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            try:
                subject = get_subject_by_code(join_code)
            except DatabaseConnectionError as exc:
                st.error(str(exc))
                return
            if subject:
                student_id = st.session_state.student_data['student_id']

                try:
                    already_enrolled = is_student_enrolled(student_id, subject['subject_id'])
                except DatabaseConnectionError as exc:
                    st.error(str(exc))
                    return
                if already_enrolled:
                    st.warning('You are already enrolled in this program')
                else:
                    try:
                        enroll_student_to_subject(student_id, subject['subject_id'])
                    except DatabaseConnectionError as exc:
                        st.error(str(exc))
                        return
                    st.success('Succesfully enrolled!')
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('Subject Code not found!')
        else:
            st.warning('Please enter a subject code')
