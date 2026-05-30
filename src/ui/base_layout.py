import streamlit as st

def style_base_layout():

    st.markdown("""
        <style>
                
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root{
            --snapclass-scale:0.675;
        }
                
        /* Hide top bar of streamlit */
                
            #MainMenu, footer, header{
                visibility:hidden;
            }
                
            .block-container{
                padding-top:1.1rem !important;
                padding-left:1rem !important;
                padding-right:1rem !important;
                max-width:1080px !important;
                margin:0 auto !important;
            }

            @media (min-width: 900px){
                .block-container{
                    zoom:var(--snapclass-scale);
                    width:calc(100% / var(--snapclass-scale)) !important;
                    max-width:calc(1080px / var(--snapclass-scale)) !important;
                }
            }
        
            h1{
                font-family:'Poppins',sans-serif !important;

                font-size:2.8rem !important;

                font-weight:700 !important;

                letter-spacing:-2px !important;

                line-height:1 !important;

                color:#ECE9FF !important;

                text-align:center;

                margin-bottom:1.2rem !important;
            }

            h2{

                font-family:'Poppins',sans-serif !important;

                font-size:1.55rem !important;

                font-weight:600 !important;

                color:#F5F3FF !important;

                text-align:center;

                margin-bottom:0.8rem !important;
            }
            

            body,
            .stApp{
                font-family:'Inter',sans-serif !important;
                color:#D6D6E7 !important;
            }
                
            .stButton > button{
                border-radius:16px !important;

                background:linear-gradient(
                    135deg,
                    #D946EF,
                    #8B5CF6
                ) !important;

                opacity:0.92;
                color:white !important;

                padding:10px 16px !important;

                border:none !important;

                font-weight:600 !important;
                font-size:0.98rem !important;

                transition:all 0.25s ease !important;

                box-shadow:0 6px 18px rgba(139,92,246,0.22);

                width:100%;
            }

            .stButton > button:hover{
                transform:translateY(-1px);

                box-shadow:0 4px 16px rgba(139,92,246,0.18);
            }  

            [data-testid="stCameraInput"] button{
                background:linear-gradient(135deg, #D946EF, #8B5CF6) !important;
                color:#F5F3FF !important;
                border:none !important;
                font-weight:600 !important;
                opacity:1 !important;
            }

            [data-testid="stCameraInput"] button:disabled{
                opacity:0.82 !important;
                color:#EEE9FF !important;
            }

            .stTextInput input{
                background:rgba(255,255,255,0.92) !important;

                border:1px solid rgba(255,255,255,0.08) !important;

                color:#111827 !important;

                -webkit-text-fill-color:#111827 !important;

                caret-color:#111827 !important;

                border-radius:14px !important;

                padding:0.72rem !important;

                font-size:14px !important;
            }

            .stTextInput label,
            .stTextInput label p{
                color:#D8CCFF !important;
                opacity:1 !important;
                font-weight:600 !important;
                letter-spacing:0.2px;
            }

            /* Placeholder */

            .stTextInput input::placeholder{
                color:#6B7280 !important;
                opacity:1 !important;
            }

            /* Focus */

            .stTextInput input:focus{
                border:1px solid #A78BFA !important;

                box-shadow:0 0 12px rgba(167,139,250,0.35) !important;

                color:#111827 !important;

                background:white !important;

                -webkit-text-fill-color:#111827 !important;
            }


            /* DATAFRAME / TABLE */

            [data-testid="stDataFrame"]{
                color:white !important;
            }

            .stTextInput input:hover{
                border:1px solid rgba(167,139,250,0.4) !important;
            }

            /* Selectbox - dark glass style for dashboard forms */
            .stSelectbox label p{
                color:#D8CCFF !important;
                font-weight:600 !important;
                letter-spacing:0.2px;
            }

            .stSelectbox div[data-baseweb="select"] > div{
                background:linear-gradient(
                    145deg,
                    rgba(20,20,38,0.94),
                    rgba(13,13,27,0.96)
                ) !important;
                border:1px solid rgba(196,181,253,0.24) !important;
                border-radius:14px !important;
                color:#F3EEFF !important;
                box-shadow:
                    0 8px 22px rgba(0,0,0,0.30),
                    0 0 0 1px rgba(139,92,246,0.10) inset !important;
                min-height:46px !important;
            }

            .stSelectbox div[data-baseweb="select"] div{
                color:#F3EEFF !important;
            }

            .stSelectbox div[data-baseweb="select"] svg{
                fill:#C4B5FD !important;
            }

            div[role="listbox"] ul{
                background:linear-gradient(
                    145deg,
                    rgba(19,19,37,0.98),
                    rgba(11,11,24,0.98)
                ) !important;
                border:1px solid rgba(196,181,253,0.28) !important;
            }

            div[role="listbox"] li{
                color:#EFE9FF !important;
            }

            div[role="listbox"] li:hover{
                background:rgba(139,92,246,0.22) !important;
            }

            div[role="listbox"] li[aria-selected="true"]{
                background:rgba(147,51,234,0.30) !important;
            }

            @media (max-width: 1100px){
                .block-container{
                    max-width:980px !important;
                }
            }
            .stApp{
                animation:fadeIn 0.6s ease;
            }

            @keyframes fadeIn{
                from{
                    opacity:0;
                    transform:translateY(10px);
                }

                to{
                    opacity:1;
                    transform:translateY(0);
                }
            }
                
            /* =========================
                MODAL / DIALOG THEME
                ========================= */

                div[role="dialog"] > div {
                    background: linear-gradient(
                        135deg,
                        rgba(10,10,25,0.98),
                        rgba(24,14,52,0.98)
                    ) !important;

                    border:1px solid rgba(255,255,255,0.08) !important;

                    border-radius:26px !important;

                    box-shadow:0 12px 40px rgba(0,0,0,0.55) !important;

                    padding:1rem !important;
                }

                /* Modal Headings */

                div[role="dialog"] h1,
                div[role="dialog"] h2,
                div[role="dialog"] h3 {
                    color:#F5F3FF !important;
                }

                /* Modal Text */

                div[role="dialog"] p,
                div[role="dialog"] label,
                div[role="dialog"] span {
                    color:#D6D6E7 !important;
                }

                /* Table */

                div[role="dialog"] table {
                    background:rgba(255,255,255,0.03) !important;
                    border-radius:14px !important;
                    overflow:hidden !important;
                }

                div[role="dialog"] th {
                    background:rgba(139,92,246,0.18) !important;
                    color:#F5F3FF !important;
                }

                div[role="dialog"] td {
                    background:rgba(255,255,255,0.02) !important;
                    color:#EAEAEA !important;
                }

                /* Modal Buttons */

                div[role="dialog"] button {
                    background:linear-gradient(
                        135deg,
                        #EC4899,
                        #8B5CF6
                    ) !important;

                    color:white !important;

                    border:none !important;

                    border-radius:16px !important;

                    font-weight:600 !important;

                    box-shadow:0 6px 18px rgba(139,92,246,0.25) !important;
                }

                /* Close Button */

                div[role="dialog"] button[aria-label="Close"] {
                    background:transparent !important;
                    box-shadow:none !important;
                }           

                div[role="dialog"] {
                    border:none !important;
                    outline:none !important;
                    background:transparent !important;
                }
                div[role="dialog"] table,
                div[role="dialog"] thead,
                div[role="dialog"] tbody,
                div[role="dialog"] tr,
                div[role="dialog"] td,
                div[role="dialog"] th {
                    background:rgba(255,255,255,0.04) !important;
                    color:#F3EEFF !important;
                    border:1px solid rgba(255,255,255,0.06) !important;
                }

                div[role="dialog"] > div {
                    width:700px !important;
                    max-width:90vw !important;
                }

                div[role="dialog"] dataframe,
                div[role="dialog"] .stDataFrame,
                div[role="dialog"] [data-testid="stTable"] {
                    background:transparent !important;
                }

                div[role="dialog"] table {
                    border-collapse:collapse !important;
                    overflow:hidden !important;
                    border-radius:14px !important;
                }

                div[role="dialog"] th {
                    background:rgba(139,92,246,0.22) !important;
                    color:#F5F3FF !important;
                    font-weight:600 !important;
                }

                div[role="dialog"] td {
                    background:rgba(255,255,255,0.03) !important;
                    color:#EAEAEA !important;
                }

                div[role="dialog"] tr:hover td {
                    background:rgba(139,92,246,0.08) !important;
                }   


        [data-testid="stDataFrame"] thead th {
            background:rgba(139,92,246,0.20) !important;

            color:#F5F3FF !important;

            font-weight:600 !important;

            border:none !important;
        }

        /* Body Cells */

        [data-testid="stDataFrame"] tbody td {
            background:rgba(255,255,255,0.03) !important;

            color:#ECECEC !important;

            border-color:rgba(255,255,255,0.05) !important;
        }

        /* Hover */

        [data-testid="stDataFrame"] tbody tr:hover td {
            background:rgba(139,92,246,0.08) !important;
        }

                
        /* =========================
            SUBJECT CARD
            ========================= */

            .subject-card{

                background:
                    linear-gradient(
                        145deg,
                        rgba(15,15,28,0.95),
                        rgba(24,24,40,0.88)
                    );

                border:1px solid rgba(255,215,120,0.18);

                border-radius:28px;

                padding:34px;

                margin-bottom:32px;

                backdrop-filter:blur(18px);

                box-shadow:
                    0 10px 35px rgba(0,0,0,0.35),
                    0 0 20px rgba(255,215,120,0.04);

                transition:0.3s ease;
            }

            .subject-card:hover{

                transform:translateY(-4px);

                border:1px solid rgba(255,215,120,0.30);

                box-shadow:
                    0 16px 40px rgba(0,0,0,0.45),
                    0 0 28px rgba(255,215,120,0.08);
            }

            .subject-title{

                text-align:center;

                font-size:2.3rem;

                font-weight:800;

                color:white;

                margin-bottom:28px;

                letter-spacing:-1px;
            }

            .subject-grid{

                display:grid;

                grid-template-columns:1fr 1fr;

                gap:22px;
            }

            .info-box{

                background:
                    linear-gradient(
                        145deg,
                        rgba(139,92,246,0.14),
                        rgba(91,33,182,0.08)
                    );

                border:1px solid rgba(255,255,255,0.06);

                border-radius:22px;

                padding:24px;
            }

            .info-label{

                color:#D8B4FE;

                font-size:1rem;

                font-weight:700;

                margin-bottom:12px;
            }

            .info-value{

                color:white;

                font-size:2.6rem;

                font-weight:900;

                line-height:1;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_home():

    st.markdown("""
        <style>

            .stApp{
                background:
                radial-gradient(
                    circle at 12% 15%,
                    rgba(168,85,247,0.75) 0%,
                    transparent 38%
                ),

                radial-gradient(
                    circle at 88% 12%,
                    rgba(139,92,246,0.45) 0%,
                    transparent 28%
                ),

                radial-gradient(
                    circle at 85% 85%,
                    rgba(251,191,36,0.20) 0%,
                    transparent 35%
                ),

                radial-gradient(
                    circle at center,
                    rgba(255,255,255,0.03) 0%,
                    transparent 60%
                ),

                linear-gradient(
                    135deg,
                    #05050A 0%,
                    #0B0B14 45%,
                    #07070D 100%
                ) !important;

                color:white;
            }

            div[data-testid="stColumn"]{

                background: rgba(22,22,29,0.72) !important;

                backdrop-filter: blur(18px);

                border: 1px solid rgba(255,255,255,0.08);

                padding:1.6rem !important;

                border-radius:2rem !important;

                box-shadow:
                0 8px 32px rgba(0,0,0,0.35);

                transition: all 0.3s ease;
            }

            .stApp div[data-testid="stColumn"]:hover{

                transform: translateY(-6px);

                border:1px solid rgba(167,139,250,0.25);

                box-shadow:
                0 12px 40px rgba(167,139,250,0.12);
            }

            .stButton > button{

                background:
                linear-gradient(
                135deg,
                #A78BFA,
                #8B5CF6
                ) !important;

                color:white !important;

                border:none !important;

                border-radius:999px !important;

                padding:0.85rem 1.6rem !important;

                font-weight:600 !important;

                transition:0.3s ease !important;
            }

            .stButton > button:hover{

                transform:translateY(-2px);

                box-shadow:
                0 10px 25px rgba(167,139,250,0.30);

                color:white !important;
            }

            

            .portal-image{
                display:flex;
                justify-content:center;
                margin-top:1rem;
                margin-bottom:1.2rem;
            }

            .portal-image img{
                width:140px;
                border:none;
                background:transparent;
            }
            .teacher-image img{
                width:165px !important;
            }

            [data-testid="stImage"]{
                text-align:center;
            }

            [data-testid="stImage"] img{
                margin:auto;
            }
        </style>
    """, unsafe_allow_html=True)

    

def style_background_dashboard():

    st.markdown("""
    <style>

    .stApp{
        background:
            radial-gradient(circle at top left,
            rgba(167,139,250,0.30),
            transparent 28%),

            radial-gradient(circle at top right,
            rgba(139,92,246,0.22),
            transparent 30%),

            radial-gradient(circle at bottom right,
            rgba(200,169,107,0.15),
            transparent 24%),

            linear-gradient(
                135deg,
                #070710 0%,
                #0B0B17 45%,
                #050507 100%
            );

        color:white;
    }

    </style>
    """, unsafe_allow_html=True)
