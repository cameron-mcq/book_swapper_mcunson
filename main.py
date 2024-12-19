import streamlit as st

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

# Hardcoded list of names
names = ["Tom", "Paul", "Sean", "Megs", "Claire", "Anne", "Cam"]

# Initialise session state variables
if "remaining_names" not in st.session_state:
    st.session_state.remaining_names = names.copy()

if "user_clicked" not in st.session_state:
    st.session_state.user_clicked = False

# Check if the user has already clicked
if st.session_state.user_clicked:
    st.image("you-didnt-say-the-magic-word-ah-ah.gif")
else:
    # Button to show a name
    if st.button("Get a Name"):
        if st.session_state.remaining_names:
            selected_name = st.session_state.remaining_names.pop(0)
            st.success(f"You are getting a book for: {selected_name}")
            st.session_state.user_clicked = True  # Mark the user as having clicked
        else:
            st.warning("No more names left!")

# Display the remaining names (optional, for testing purposes)
st.write("Remaining names:", st.session_state.remaining_names)
