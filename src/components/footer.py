import streamlit as st


def footer_home():
    st.markdown(
        (
            "<div style='text-align:center;color:rgba(245,243,255,0.92);margin-top:32px;"
            "margin-bottom:6px;font-size:0.95rem;letter-spacing:0.2px;'>"
            "Created with &#10084; by <b>Tanmayee</b></div>"
        ),
        unsafe_allow_html=True,
    )


def footer_dashboard():
    st.markdown(
        (
            "<div style='text-align:center;color:rgba(237,233,255,0.94);margin-top:28px;"
            "margin-bottom:14px;font-size:0.96rem;letter-spacing:0.25px;"
            "text-shadow:0 1px 10px rgba(0,0,0,0.45);'>"
            "Created with  &#10084; by <b>Tanmayee</b></div>"
        ),
        unsafe_allow_html=True,
    )
