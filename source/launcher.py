import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Driver Drowsiness Detection System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create sidebar navigation
with st.sidebar:
    st.title("🚗 Navigation")
    st.markdown("---")
    selected = st.radio(
        "Select Page:",
        ["🎥 Drowsiness Detection", "⚙️ Configuration"],
        help="Choose between running the detection system or configuring PERCLOS thresholds"
    )
    st.markdown("---")
    st.info("💡 **Tip**: Configure PERCLOS thresholds before running detection for optimal results.")

# Route to appropriate page
if selected == "🎥 Drowsiness Detection":
    st.title("🎥 Driver Drowsiness Detection")
    st.info("💡 Use the configuration page to adjust PERCLOS thresholds before running detection.")
    st.markdown("---")
    
    # Import and run the main app
    try:
        import app
        app.play_webcam()
    except Exception as e:
        st.error(f"Error loading detection module: {e}")
        st.info("Make sure all dependencies are installed. Check requirements.txt")

elif selected == "⚙️ Configuration":
    # Import and run the config page
    try:
        import config_page
        config_page.create_config_page()
    except Exception as e:
        st.error(f"Error loading configuration module: {e}")
