import streamlit as st
import base64
import html as py_html


# convert img file into base64 string
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def header_home():
    logo_path = "assets/logo.png"

    # logo
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:center;
            width:100%;
            margin-top:6px;
            margin-bottom:8px;
        ">
            <img src="data:image/png;base64,{get_base64_image(logo_path)}"
                 width="112">
        </div>
        """,
        unsafe_allow_html=True
    )

    # title + css
    st.markdown(
        """
        <style>
        .snapclass-title {
            text-align: center;
            font-family: Poppins, sans-serif;
            font-size: 56px;
            font-weight: 700;
            letter-spacing: -3px;
            margin-top: -6px;
            margin-bottom: 0px;

            background: linear-gradient(
                135deg,
                #FFFFFF,
                #C4B5FD,
                #8B5CF6
            );

            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .snapclass-tagline {
            text-align: center;
            color: #B8B2CC;
            font-size: 16px;
            margin-top: 6px;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
            text-shadow: 0 1px 8px rgba(0,0,0,0.25);
        }
        </style>

        <div class="snapclass-title">
            SNAPCLASS
        </div>

        <p class="snapclass-tagline">
            AI-Powered Smart Attendance Platform
        </p>
        """,
        unsafe_allow_html=True
    )


def header_dashboard(title="Teacher Dashboard"):
    safe_title = py_html.escape(str(title))

    st.markdown(
        f"""
        <h1 style="
            font-size:2.2rem;
            font-weight:700;
            color:#A78BFA;
            margin-bottom:0.2rem;
            white-space:nowrap;
        ">
            {safe_title}
        </h1>
        """,
        unsafe_allow_html=True
    )