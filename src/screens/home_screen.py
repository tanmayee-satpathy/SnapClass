import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout,style_background_home

def home_screen():

    header_home() # logo, navbar , heading

    style_background_home()
    style_base_layout()

    col1, col2 = st.columns([1,1], gap="medium")

    with col1:

        st.header("I'm Student")

        st.markdown("""
        <div class="portal-image">
            <img src="https://i.ibb.co/844D9Lrt/mascot-student.png">
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Student Portal",
            type="primary",
            icon=':material/arrow_outward:',
            use_container_width=True # button use full column width
        ):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:

        st.header("I'm Teacher")

        st.markdown("""
        <div class="portal-image teacher-image">
            <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png">
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Teacher Portal",
            type="primary",
            icon=':material/arrow_outward:',
            use_container_width=True
        ):
            st.session_state['login_type'] = 'teacher'
            st.rerun()


    # add vertical space before footer
    st.markdown("<br><br>", unsafe_allow_html=True)

    footer_home()