import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Co-op Data')