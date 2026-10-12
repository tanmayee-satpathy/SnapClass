import streamlit as st
import socket
from urllib.parse import urlparse
from supabase import create_client,Client

url = st.secrets["SUPABASE_URL"]
hostname = urlparse(url).hostname

try:
    print("Supabase hostname:", hostname)
    print("Resolved addresses:", socket.getaddrinfo(hostname, 443))
except Exception:
    import logging
    logging.exception("SUPABASE DNS RESOLUTION FAILED")
    
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)