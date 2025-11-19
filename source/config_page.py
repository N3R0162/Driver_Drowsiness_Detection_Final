import streamlit as st
import json
import os

# Global config file path
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'perclos_config.json')

def load_config_from_file():
    """Load configuration from JSON file"""
    default_config = {
        'semi_closed_min': 0.0,
        'semi_closed_max': 3.75,
        'moderately_drowsy_min': 3.75,
        'moderately_drowsy_max': 10.0,
        'drowsy_min': 10.0,
        'drowsy_max': 15.0,
        'very_drowsy_min': 15.0,
        'very_drowsy_max': 20.0,
        'sleeping_min': 20.0,
        'ear_thresh': 0.15,
        'sleep_threshold': 3.0,
        'perclos_time_period': 60,
        'audio_files': {
            'Semi-Closed': 'Semi-closed.mp3',
            'Moderately Drowsy': 'Moderate_Drowsiness.mp3',
            'Drowsy': 'Drowsiness.mp3',
            'Sleeping': 'Sleep.mp3'
        }
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Error loading config: {e}. Using defaults.")
            return default_config
    return default_config

def save_config_to_file(config):
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving config: {e}")
        return False

def get_config():
    """Get configuration from session state (persistent across page changes)"""
    # Initialize session state on first run
    if 'perclos_config' not in st.session_state:
        st.session_state.perclos_config = load_config_from_file()
    return st.session_state.perclos_config

def update_config(new_config):
    """Update configuration in both session state and file"""
    st.session_state.perclos_config = new_config
    return save_config_to_file(new_config)


def create_config_page():
    """Create the Streamlit configuration page with session state persistence"""
    
    st.title("⚙️ PERCLOS Score Configuration")
    st.markdown("---")
    
    # Get config from session state (persists across page changes)
    config = get_config()
    
    # Show current config file status
    if os.path.exists(CONFIG_FILE):
        st.success("✅ Configuration loaded from session state (persists across pages)")
    else:
        st.warning("⚠️ No configuration file found. Using default values.")
    
    st.markdown("""
    ### About PERCLOS (Percentage of Eye Closure)
    PERCLOS is a measure of drowsiness based on how often and how long eyes are closed over time.
    Configure the threshold ranges below to customize alertness detection levels.
    
    **💾 Changes are saved to session state immediately and persist when switching pages!**
    """)
    
    st.markdown("---")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 Awake State")
        st.info("Driver is fully alert and awake")
        awake_max = st.slider(
            "Maximum PERCLOS Score for Awake",
            min_value=0.0,
            max_value=10.0,
            value=float(config.get('semi_closed_max', 3.75)),
            step=0.25,
            help="Below this value, the driver is considered awake",
            key="awake_max"
        )
        
        st.markdown("---")
        
        st.subheader("🟡 Semi-Closed State")
        st.warning("Driver is showing early signs of drowsiness")
        semi_closed_min = awake_max
        semi_closed_max = st.slider(
            "Maximum PERCLOS Score for Semi-Closed",
            min_value=awake_max,
            max_value=20.0,
            value=float(max(config.get('moderately_drowsy_max', 10.0), awake_max + 0.25)),
            step=0.25,
            help="Eyes are starting to close more frequently",
            key="semi_closed_max"
        )
        
        st.markdown("---")
        
        st.subheader("🟠 Moderately Drowsy State")
        st.warning("Driver is moderately drowsy - caution advised")
        moderately_drowsy_min = semi_closed_max
        moderately_drowsy_max = st.slider(
            "Maximum PERCLOS Score for Moderately Drowsy",
            min_value=semi_closed_max,
            max_value=25.0,
            value=float(max(config.get('drowsy_max', 15.0), semi_closed_max + 0.25)),
            step=0.25,
            help="Driver should take a break soon",
            key="moderately_drowsy_max"
        )
    
    with col2:
        st.subheader("🔴 Drowsy State")
        st.error("Driver is significantly drowsy - immediate action needed")
        drowsy_min = moderately_drowsy_max
        drowsy_max = st.slider(
            "Maximum PERCLOS Score for Drowsy",
            min_value=moderately_drowsy_max,
            max_value=30.0,
            value=float(max(config.get('very_drowsy_max', 20.0), moderately_drowsy_max + 0.25)),
            step=0.25,
            help="Driver must take a break immediately",
            key="drowsy_max"
        )
        
        st.markdown("---")
        
        st.subheader("⚫ Very Drowsy State")
        st.error("Driver is extremely drowsy - critical condition")
        very_drowsy_min = drowsy_max
        very_drowsy_max = st.slider(
            "Maximum PERCLOS Score for Very Drowsy",
            min_value=drowsy_max,
            max_value=35.0,
            value=float(max(config.get('sleeping_min', 25.0), drowsy_max + 0.25)),
            step=0.25,
            help="Critical drowsiness level",
            key="very_drowsy_max"
        )
        
        st.markdown("---")
        
        st.subheader("💤 Sleeping State")
        st.error("Driver is sleeping - EMERGENCY")
        sleeping_min = very_drowsy_max
        st.metric("Sleeping State Threshold", f"{sleeping_min:.2f}+")
        st.caption("Any score above this threshold indicates the driver is sleeping")
    
    st.markdown("---")
    
    # Advanced Detection Parameters
    st.subheader("🔧 Advanced Detection Parameters")
    
    param_col1, param_col2, param_col3 = st.columns(3)
    
    with param_col1:
        st.markdown("**👁️ EAR Threshold**")
        ear_thresh = st.slider(
            "Eye Aspect Ratio",
            min_value=0.05,
            max_value=0.30,
            value=float(config.get('ear_thresh', 0.15)),
            step=0.01,
            help="Lower values = eyes considered closed more easily",
            key="ear_thresh"
        )
        st.caption(f"Current: {ear_thresh:.2f}")
    
    with param_col2:
        st.markdown("**😴 Sleep Threshold**")
        sleep_threshold = st.slider(
            "Continuous Closure (seconds)",
            min_value=0.5,
            max_value=10.0,
            value=float(config.get('sleep_threshold', 3.0)),
            step=0.5,
            help="Duration of continuous eye closure to trigger sleep alert",
            key="sleep_threshold"
        )
        st.caption(f"Current: {sleep_threshold:.1f}s")
    
    with param_col3:
        st.markdown("**⏱️ PERCLOS Time Period**")
        perclos_time_period = st.slider(
            "Time Period (seconds)",
            min_value=10,
            max_value=120,
            value=int(config.get('perclos_time_period', 60)),
            step=5,
            help="Time window for PERCLOS calculation",
            key="perclos_time_period"
        )
        st.caption(f"Current: {perclos_time_period}s")
    
    st.markdown("---")
    
    # Audio Configuration section remains the same...
    st.subheader("🔊 Audio Alert Configuration")    
    audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    available_audio_files = ['None']
    if os.path.exists(audio_dir):
        available_audio_files.extend([f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav', '.ogg'))])
    
    current_audio = config.get('audio_files', {
        'Semi-Closed': 'Semi-closed.mp3',
        'Moderately Drowsy': 'Moderate_Drowsiness.mp3',
        'Drowsy': 'Drowsiness.mp3',
        'Sleeping': 'Sleep.mp3'
    })
    
    # File upload section
    with st.expander("📤 Upload New Audio Files", expanded=False):
        st.markdown("Upload audio files (.mp3, .wav, .ogg) to add them to your collection.")
        
        upload_col1, upload_col2 = st.columns([3, 1])
        
        with upload_col1:
            uploaded_files = st.file_uploader(
                "Choose audio files",
                type=['mp3', 'wav', 'ogg'],
                accept_multiple_files=True,
                help="Upload one or more audio files to the audio directory",
                key="audio_uploader"
            )
        
        with upload_col2:
            if uploaded_files:
                if st.button("💾 Save Uploaded Files", use_container_width=True):
                    saved_files = []
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(audio_dir, uploaded_file.name)
                        with open(file_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        saved_files.append(uploaded_file.name)
                    
                    st.success(f"✅ Saved {len(saved_files)} file(s)")
                    st.rerun()
        
        if uploaded_files:
            st.markdown("**Files to upload:**")
            for uploaded_file in uploaded_files:
                st.text(f"  📁 {uploaded_file.name}")
    
    audio_col1, audio_col2 = st.columns(2)
    
    with audio_col1:
        st.markdown("**🟡 Semi-Closed Alert**")
        semi_closed_audio = st.selectbox(
            "Audio file for Semi-Closed state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Semi-Closed', 'Semi-closed.mp3')) if current_audio.get('Semi-Closed', 'Semi-closed.mp3') in available_audio_files else 0,
            key="semi_closed_audio"
        )
        
        st.markdown("**🟠 Moderately Drowsy Alert**")
        moderately_drowsy_audio = st.selectbox(
            "Audio file for Moderately Drowsy state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Moderately Drowsy', 'Moderate_Drowsiness.mp3')) if current_audio.get('Moderately Drowsy', 'Moderate_Drowsiness.mp3') in available_audio_files else 0,
            key="moderately_drowsy_audio"
        )
    
    with audio_col2:
        st.markdown("**🔴 Drowsy Alert**")
        drowsy_audio = st.selectbox(
            "Audio file for Drowsy state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Drowsy', 'Drowsiness.mp3')) if current_audio.get('Drowsy', 'Drowsiness.mp3') in available_audio_files else 0,
            key="drowsy_audio"
        )
        
        st.markdown("**💤 Sleeping Alert**")
        sleeping_audio = st.selectbox(
            "Audio file for Sleeping state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Sleeping', 'Sleep.mp3')) if current_audio.get('Sleeping', 'Sleep.mp3') in available_audio_files else 0,
            key="sleeping_audio"
        )
    
    with st.expander("📁 Manage Audio Files", expanded=False):
        if len(available_audio_files) > 1:
            st.write(f"**Found {len(available_audio_files)-1} audio files:**")
            
            for audio_file in available_audio_files[1:]:
                file_col1, file_col2, file_col3 = st.columns([3, 1, 1])
                
                with file_col1:
                    st.text(f"🎵 {audio_file}")
                
                with file_col2:
                    audio_path = os.path.join(audio_dir, audio_file)
                    if os.path.exists(audio_path):
                        try:
                            with open(audio_path, 'rb') as audio_file_obj:
                                audio_bytes = audio_file_obj.read()
                            st.audio(audio_bytes, format=f'audio/{audio_file.split(".")[-1]}')
                        except:
                            st.caption("Preview unavailable")
                
                with file_col3:
                    if st.button("🗑️", key=f"delete_{audio_file}"):
                        try:
                            os.remove(os.path.join(audio_dir, audio_file))
                            st.success(f"Deleted {audio_file}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.warning("No audio files found. Upload some files above!")
    
    st.markdown("---")
    
    # Display summary
    st.subheader("📊 Current Configuration Summary")
    
    st.markdown("##### PERCLOS Thresholds")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("🟢 Awake", f"0.00 - {awake_max:.2f}")
        st.metric("🟡 Semi-Closed", f"{semi_closed_min:.2f} - {semi_closed_max:.2f}")
    
    with summary_col2:
        st.metric("🟠 Moderately Drowsy", f"{moderately_drowsy_min:.2f} - {moderately_drowsy_max:.2f}")
        st.metric("🔴 Drowsy", f"{drowsy_min:.2f} - {drowsy_max:.2f}")
    
    with summary_col3:
        st.metric("⚫ Very Drowsy", f"{very_drowsy_min:.2f} - {very_drowsy_max:.2f}")
        st.metric("💤 Sleeping", f"{sleeping_min:.2f}+")
    
    st.markdown("##### Detection Parameters")
    param_summary_col1, param_summary_col2, param_summary_col3 = st.columns(3)
    
    with param_summary_col1:
        st.metric("👁️ EAR Threshold", f"{ear_thresh:.2f}")
    
    with param_summary_col2:
        st.metric("😴 Sleep Threshold", f"{sleep_threshold:.1f}s")
    
    with param_summary_col3:
        st.metric("⏱️ PERCLOS Period", f"{perclos_time_period}s")
    
    st.markdown("##### Audio Configuration")
    audio_summary_col1, audio_summary_col2 = st.columns(2)
    
    with audio_summary_col1:
        st.metric("🟡 Semi-Closed", semi_closed_audio if semi_closed_audio != 'None' else '🔇 Disabled')
        st.metric("🟠 Moderately Drowsy", moderately_drowsy_audio if moderately_drowsy_audio != 'None' else '🔇 Disabled')
    
    with audio_summary_col2:
        st.metric("🔴 Drowsy", drowsy_audio if drowsy_audio != 'None' else '🔇 Disabled')
        st.metric("💤 Sleeping", sleeping_audio if sleeping_audio != 'None' else '🔇 Disabled')
    
    st.markdown("---")
    
    # Save and Reset buttons
    button_col1, button_col2, button_col3 = st.columns([1, 1, 3])
    
    with button_col1:
        if st.button("💾 Save to File", type="primary", use_container_width=True):
            # Build config
            audio_files_config = {}
            if semi_closed_audio != 'None':
                audio_files_config['Semi-Closed'] = semi_closed_audio
            if moderately_drowsy_audio != 'None':
                audio_files_config['Moderately Drowsy'] = moderately_drowsy_audio
            if drowsy_audio != 'None':
                audio_files_config['Drowsy'] = drowsy_audio
            if sleeping_audio != 'None':
                audio_files_config['Sleeping'] = sleeping_audio
            
            new_config = {
                'semi_closed_min': 0.0,
                'semi_closed_max': awake_max,
                'moderately_drowsy_min': semi_closed_min,
                'moderately_drowsy_max': semi_closed_max,
                'drowsy_min': moderately_drowsy_min,
                'drowsy_max': moderately_drowsy_max,
                'very_drowsy_min': drowsy_min,
                'very_drowsy_max': very_drowsy_max,
                'sleeping_min': sleeping_min,
                'ear_thresh': ear_thresh,
                'sleep_threshold': sleep_threshold,
                'perclos_time_period': perclos_time_period,
                'audio_files': audio_files_config
            }
            
            if update_config(new_config):
                st.success("✅ Configuration saved to file and session state!")
                st.balloons()
            else:
                st.error("❌ Failed to save configuration to file")
    
    with button_col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            default_config = load_config_from_file.__defaults__[0] if hasattr(load_config_from_file, '__defaults__') else {
                'semi_closed_min': 0.0,
                'semi_closed_max': 3.75,
                'moderately_drowsy_min': 3.75,
                'moderately_drowsy_max': 10.0,
                'drowsy_min': 10.0,
                'drowsy_max': 15.0,
                'very_drowsy_min': 15.0,
                'very_drowsy_max': 20.0,
                'sleeping_min': 20.0,
                'ear_thresh': 0.15,
                'sleep_threshold': 3.0,
                'perclos_time_period': 60,
                'audio_files': {
                    'Semi-Closed': 'Semi-closed.mp3',
                    'Moderately Drowsy': 'Moderate_Drowsiness.mp3',
                    'Drowsy': 'Drowsiness.mp3',
                    'Sleeping': 'Sleep.mp3'
                }
            }
            
            if update_config(default_config):
                st.success("✅ Configuration reset to defaults!")
                st.rerun()
            else:
                st.error("❌ Failed to reset configuration")
    
    st.info("💡 **Tip:** Your changes are automatically preserved when switching pages. Click 'Save to File' to make them permanent!")


if __name__ == "__main__":
    create_config_page()