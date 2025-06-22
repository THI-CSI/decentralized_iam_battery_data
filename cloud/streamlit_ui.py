import base64
import streamlit as st
import requests
import qrcode
import os
import re

from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

# Dynamic API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
STREAMLIT_BASE_URL = os.getenv("STREAMLIT_BASE_URL", "http://localhost:8501")

st.title(":green[BatteryPass Data Viewer]")

# Hide Deploy Button
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar options to interact with the API
st.sidebar.title("Options")
view_data = st.sidebar.selectbox(
    "What would you like to do?",
    ["List All DIDs", "Retrieve Battery Pass Data"],
    on_change=lambda: st.query_params.pop("did") if "did" in st.query_params else None
)

query_params = st.query_params
did = query_params.get("did")
if did:
    view_data = "Retrieve Battery Pass Data"


def prettify_camel_case(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text).title()


def render_item(value, indent=0):
    prefix = "&nbsp;" * 4 * indent

    if isinstance(value, dict):
        for sub_key, sub_val in value.items():
            display_key = prettify_camel_case(sub_key)
            if isinstance(sub_val, (dict, list)):
                st.markdown(f"{prefix}**{display_key}:**")
                render_item(sub_val, indent + 1)
            else:
                if isinstance(sub_val, str) and sub_val.startswith(("http://", "https://", "ftp://", "telnet://")):
                    st.markdown(f'{prefix}**{display_key}:** [{sub_val}]({sub_val})')
                else:
                    st.markdown(f"{prefix}**{display_key}:** {sub_val}")

    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                render_item(item, indent)
                st.markdown("")  # Spacer
            else:
                st.markdown(f"{prefix}- {item}")


def render_top_level(data):
    for key, value in data.items():
        display_key = prettify_camel_case(key)
        with st.expander(f":green[{display_key}]", expanded=False):
            render_item(value)


# Function to fetch all DIDs
def list_all_dids():
    url = f"{API_BASE_URL}/batterypass/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        st.error(f"Could not connect to the API: {e}")
        return []


# Function to fetch data for a specific DID
def fetch_did_data(did):
    url = f"{API_BASE_URL}/batterypass/{did}"
    try:
        response = requests.post(f"{API_BASE_URL}/batterypass/read/{did}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        st.error(f"Could not connect to the API: {e}")
        return None


def generate_qr_code() -> BytesIO:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(front_color=(50, 100, 60), back_color=(255, 255, 255))
    )
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return buf


# List All DIDs
if view_data == "List All DIDs":
    st.header("List of All Available DIDs")
    dids = list_all_dids()
    if dids:
        st.write("Available DIDs in the database:")
        for did in dids:
            st.markdown(
                f"""
                    <style>
                    .hover-link {{
                        text-decoration: none !important;
                        color: #6ed278 !important;
                        transition: color 0.2s ease;
                    }}
                    .hover-link:hover {{
                        color: white !important;
                    }}
                    </style>
    
                    - <a href="{STREAMLIT_BASE_URL}/?did={did}" class="hover-link" target="_blank">{did}</a>
                """
                , unsafe_allow_html=True)
    else:
        st.warning("No DIDs found in the database.")

# Retrieve and Display Data for a DID
elif view_data == "Retrieve Battery Pass Data":
    st.header("Retrieve Battery Pass Data for a Specific DID")
    did_input = st.text_input("Enter a DID to fetch its data:", value=did)
    if did_input and did_input.strip():
        data = fetch_did_data(did_input.strip())
        if data:
            url = f"{STREAMLIT_BASE_URL}/?did={did_input.strip()}"
            buf = generate_qr_code()
            st.markdown(f'#### Data for **:green[{did_input.strip()}]**',
                        unsafe_allow_html=True)
            st.markdown(
                f"""
                        <div style='text-align: left;'>
                            <img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}' 
                            style='border-radius: 10%;' alt='QR Code;'/>
                            <br><br>
                            <p>Scan the QR code to open this page in your browser.</p>
                        </div>
                    """,
                unsafe_allow_html=True)
            st.markdown("")
            render_top_level(data)
    else:
        st.warning("Please enter a valid DID.")
