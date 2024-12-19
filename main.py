import streamlit as st
from streamlit_server_state import server_state, server_state_lock

# Function to load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load local CSS
local_css("style/style.css")

# Snowflake animation
animation_symbol = "❄"

st.markdown(
    f"""
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    """,
    unsafe_allow_html=True,
)

# Centre-align content using custom CSS
st.markdown(
    """
    <style>
     body {
        background-color: black;
    }
    div.block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("McUnSon Book Swapper")

# Initialise global state for remaining names using server_state
with server_state_lock["remaining_names"]:  # Lock the "remaining_names" state for thread-safety
    if "remaining_names" not in server_state:
        server_state.remaining_names = ["Tom", "Paul", "Sean", "Megs", "Claire", "Anne", "Cam"]

# Check if the user has already clicked
if "user_clicked" not in server_state:
    server_state.user_clicked = False

# Check if the user has already clicked
if server_state.user_clicked:
    st.image("you-didnt-say-the-magic-word-ah-ah.gif")
else:
    # Button to show a name
    if st.button("Get a Name"):
        with server_state_lock["remaining_names"]:
            if server_state.remaining_names:
                selected_name = server_state.remaining_names.pop(0)
                st.success(f"You are getting a book for: {selected_name}")
                server_state.user_clicked = True  # Mark the user as having clicked
            else:
                st.warning("No more names left!")

# Display the current global state count (for debug purposes)
st.write("Remaining names:", server_state.remaining_names)
