import streamlit as st
import random
import os


# Function to load local CSS with error handling
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Provide default CSS if file not found
        st.markdown("""
            <style>
                body {
                    background-color: black;
                }
                .snowflake {
                    color: white;
                    font-size: 1em;
                    font-family: Arial, sans-serif;
                    text-shadow: 0 0 5px #000;
                }
            </style>
        """, unsafe_allow_html=True)


# Try to load local CSS, fall back to defaults if not found
try:
    local_css("style/style.css")
except Exception as e:
    st.warning("Style file not found, using default styling")

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

# File paths
remaining_names_path = "remaining_names.txt"
names_used_path = "names_used.txt"


# Ensure the files exist
def ensure_file_exists(filepath, default_content=[]):
    """Create file if it doesn't exist"""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            if isinstance(default_content, list):
                f.writelines([f"{item}\n" for item in default_content])
            elif isinstance(default_content, dict):
                for k, v in default_content.items():
                    f.write(f"{k}:{v}\n")


# Default users list
default_users = ["Tom", "Paul", "Sean", "Megs", "Claire", "Anne", "Cam", "Granny Cake"]

# Ensure files exist before trying to read them
ensure_file_exists(remaining_names_path, default_users)
ensure_file_exists(names_used_path, {})

# Initialize session state variables
if "remaining_names" not in st.session_state:
    with open(remaining_names_path, 'r') as file:
        st.session_state.remaining_names = [name.strip() for name in file.readlines() if name.strip()]

if "names_used" not in st.session_state:
    with open(names_used_path, 'r') as file:
        st.session_state.names_used = {
            line.strip().split(':')[0]: line.strip().split(':')[1]
            for line in file.readlines()
            if ':' in line
        }

# Get all available users
all_users = default_users  # Using the same list for consistency

# User selection dropdown
selected_user = st.selectbox("Select your name:", all_users)

# Check if user has already generated a name
user_already_generated = selected_user in st.session_state.names_used

if user_already_generated:
    try:
        st.image("you-didnt-say-the-magic-word-ah-ah.gif")
    except Exception as e:
        st.error("⚠️ You've already selected a name!")
    st.warning(f"You already have a name!")
else:
    # Button to generate a name
    if st.button("Generate Name"):
        if st.session_state.remaining_names:
            # Get a name that isn't the user's own name
            valid_names = [name for name in st.session_state.remaining_names if name != selected_user]

            if not valid_names:
                st.warning("Only your own name remains in the pool. Please contact the administrator!")
            else:
                # Remove the selected name from the original list
                generated_name = random.choice(valid_names)
                st.session_state.remaining_names.remove(generated_name)

                # Record the assignment
                st.session_state.names_used[selected_user] = generated_name

                try:
                    # Update remaining_names.txt
                    with open(remaining_names_path, 'w') as file:
                        file.writelines([name + "\n" for name in st.session_state.remaining_names])

                    # Update names_used.txt
                    with open(names_used_path, 'a') as file:
                        file.write(f"{selected_user}:{generated_name}\n")

                    st.success(f"{selected_user}, you are getting a book for: {generated_name}")
                except Exception as e:
                    st.error(f"Error saving to files. Please contact administrator. Error: {str(e)}")
        else:
            st.warning("No more names left!")

# For debugging purposes (comment out in production)
# st.write("Remaining names:", st.session_state.remaining_names)
# st.write("Names used:", st.session_state.names_used)
