import streamlit as st
import json
import os

class ConfigManager:
    """Manages configuration for PERCLOS thresholds"""
    
    def __init__(self, config_file='perclos_config.json'):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.default_config = {
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
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                st.warning(f"Error loading config: {e}. Using defaults.")
                self.config = self.default_config.copy()
        else:
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving config: {e}")
            return False
    
    def get_config(self):
        """Get current configuration"""
        return self.config
    
    def update_config(self, new_config):
        """Update configuration"""
        self.config = new_config


def create_config_page():
    """Create the Streamlit configuration page"""
    
    st.title("⚙️ PERCLOS Score Configuration")
    st.markdown("---")
    
    # Add status indicator
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    # Show current config file status
    config_file_path = os.path.join(os.path.dirname(__file__), 'perclos_config.json')
    if os.path.exists(config_file_path):
        st.success("✅ Configuration file loaded successfully")
    else:
        st.warning("⚠️ No configuration file found. Using default values.")
    st.markdown("""
    ### About PERCLOS (Percentage of Eye Closure)
    PERCLOS is a measure of drowsiness based on how often and how long eyes are closed over time.
    Configure the threshold ranges below to customize alertness detection levels.
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
            value=config['semi_closed_max'],
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
            value=max(config['moderately_drowsy_max'], awake_max + 0.25),
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
            value=max(config['drowsy_max'], semi_closed_max + 0.25),
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
            value=max(config['very_drowsy_max'], moderately_drowsy_max + 0.25),
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
            max_value=40.0,
            value=max(config['sleeping_min'], drowsy_max + 0.25),
            step=0.25,
            help="Extremely dangerous - vehicle should be stopped",
            key="very_drowsy_max"
        )
        
        st.markdown("---")
        
        st.subheader("💤 Sleeping State")
        st.error("Driver is sleeping or near-sleeping - emergency situation")
        sleeping_min = very_drowsy_max
        st.metric(
            "Minimum PERCLOS Score for Sleeping",
            f"{sleeping_min:.2f}",
            help="Above this value, the driver is considered sleeping"
        )
    
    st.markdown("---")
    
    # Additional Detection Parameters
    st.subheader("⚙️ Advanced Detection Parameters")
    
    param_col1, param_col2, param_col3 = st.columns(3)
    
    with param_col1:
        st.markdown("**👁️ Eye Aspect Ratio Threshold**")
        ear_thresh = st.slider(
            "EAR Threshold",
            min_value=0.0,
            max_value=0.5,
            value=config.get('ear_thresh', 0.15),
            step=0.01,
            help="Eyes are considered closed when EAR falls below this value. Lower = more sensitive",
            key="ear_thresh"
        )
        st.caption(f"Current: {ear_thresh:.2f}")
    
    with param_col2:
        st.markdown("**😴 Continuous Sleep Threshold**")
        sleep_threshold = st.slider(
            "Sleep Threshold (seconds)",
            min_value=1.0,
            max_value=10.0,
            value=config.get('sleep_threshold', 3.0),
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
    
    # Audio File Configuration
    st.subheader("🔊 Audio Alert Configuration")    
    # Get list of available audio files
    audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    available_audio_files = ['None']  # Option to disable audio
    if os.path.exists(audio_dir):
        available_audio_files.extend([f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav', '.ogg'))])
    
    # Get current audio configuration
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
                    for filename in saved_files:
                        st.text(f"  • {filename}")
                    st.info("🔄 Please refresh the page to see new files in dropdowns")
                    st.rerun()
        
        if uploaded_files:
            st.markdown("**Files to upload:**")
            for uploaded_file in uploaded_files:
                st.text(f"  📁 {uploaded_file.name} ({uploaded_file.size} bytes)")
    
    audio_col1, audio_col2 = st.columns(2)
    
    with audio_col1:
        st.markdown("**🟡 Semi-Closed Alert**")
        semi_closed_audio = st.selectbox(
            "Audio file for Semi-Closed state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Semi-Closed', 'Semi-closed.mp3')) if current_audio.get('Semi-Closed', 'Semi-closed.mp3') in available_audio_files else 0,
            key="semi_closed_audio",
            help="Plays when driver enters semi-closed eye state"
        )
        
        st.markdown("**🟠 Moderately Drowsy Alert**")
        moderately_drowsy_audio = st.selectbox(
            "Audio file for Moderately Drowsy state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Moderately Drowsy', 'Moderate_Drowsiness.mp3')) if current_audio.get('Moderately Drowsy', 'Moderate_Drowsiness.mp3') in available_audio_files else 0,
            key="moderately_drowsy_audio",
            help="Plays when driver shows moderate drowsiness"
        )
    
    with audio_col2:
        st.markdown("**🔴 Drowsy Alert**")
        drowsy_audio = st.selectbox(
            "Audio file for Drowsy state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Drowsy', 'Drowsiness.mp3')) if current_audio.get('Drowsy', 'Drowsiness.mp3') in available_audio_files else 0,
            key="drowsy_audio",
            help="Plays when driver is significantly drowsy"
        )
        
        st.markdown("**💤 Sleeping Alert**")
        sleeping_audio = st.selectbox(
            "Audio file for Sleeping state",
            available_audio_files,
            index=available_audio_files.index(current_audio.get('Sleeping', 'Sleep.mp3')) if current_audio.get('Sleeping', 'Sleep.mp3') in available_audio_files else 0,
            key="sleeping_audio",
            help="Plays when driver is sleeping or eyes closed continuously"
        )
    
    # Show available audio files with management options
    with st.expander("📁 Manage Audio Files", expanded=False):
        if len(available_audio_files) > 1:
            st.write(f"**Found {len(available_audio_files)-1} audio files:**")
            
            # Create a table-like display with delete buttons
            for audio_file in available_audio_files[1:]:  # Skip 'None'
                file_col1, file_col2, file_col3 = st.columns([3, 1, 1])
                
                with file_col1:
                    st.text(f"🎵 {audio_file}")
                
                with file_col2:
                    # Audio player for preview
                    audio_path = os.path.join(audio_dir, audio_file)
                    if os.path.exists(audio_path):
                        try:
                            with open(audio_path, 'rb') as audio_file_obj:
                                audio_bytes = audio_file_obj.read()
                            st.audio(audio_bytes, format=f'audio/{audio_file.split(".")[-1]}')
                        except Exception as e:
                            st.caption("Preview unavailable")
                
                with file_col3:
                    # Delete button
                    if st.button("🗑️", key=f"delete_{audio_file}", help=f"Delete {audio_file}"):
                        try:
                            os.remove(os.path.join(audio_dir, audio_file))
                            st.success(f"Deleted {audio_file}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.warning("No audio files found. Upload some files above!")
            st.info("Default files: Semi-closed.mp3, Moderate_Drowsiness.mp3, Drowsiness.mp3, Sleep.mp3")
    
    st.markdown("---")
    
    # Display current configuration summary
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
        if st.button("💾 Save Configuration", type="primary", use_container_width=True):
            # Build audio files dictionary, excluding 'None' selections
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
            config_manager.update_config(new_config)
            if config_manager.save_config():
                st.success("✅ Configuration saved successfully!")
            else:
                st.error("❌ Failed to save configuration")
    
    with button_col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            config_manager.config = config_manager.default_config.copy()
            if config_manager.save_config():
                st.success("✅ Configuration reset to defaults!")
                st.rerun()
            else:
                st.error("❌ Failed to reset configuration")
    
    st.markdown("---")
    
    # Additional information
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        ### Instructions:
        
        1. **Adjust Sliders**: Use the sliders to set threshold values for each drowsiness level
        2. **Preview Changes**: See the summary of your configuration in the summary section
        3. **Save Configuration**: Click the "Save Configuration" button to apply your changes
        4. **Reset to Defaults**: Click "Reset to Defaults" to restore original values
        
        ### Important Notes:
        
        - Each threshold must be higher than the previous one
        - The system automatically enforces minimum values to maintain logical progression
        - Changes will take effect in the main application after saving
        - PERCLOS scores are calculated as a percentage over a time period
        
        ### Recommended Values:
        
        - **Awake**: 0.00 - 3.75
        - **Semi-Closed**: 3.75 - 10.00
        - **Moderately Drowsy**: 10.00 - 15.00
        - **Drowsy**: 15.00 - 20.00
        - **Very Drowsy**: 20.00 - 25.00
        - **Sleeping**: 25.00+
        """)
    
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        ### PERCLOS Calculation:
        
        PERCLOS (Percentage of Eye Closure) is calculated as:
        
        ```
        PERCLOS = (Number of frames with closed eyes / Total frames in time period) × 100
        ```
        
        ### Detection Parameters:
        
        - **EAR Threshold (Eye Aspect Ratio)**: 
          - Determines when eyes are considered "closed"
          - Calculated from eye landmark positions
          - Lower values = more sensitive detection
          - Default: 0.15
        
        - **Sleep Threshold**: 
          - Duration of continuous eye closure to trigger sleep alert
          - Measured in seconds
          - Default: 3.0 seconds
        
        - **PERCLOS Time Period**: 
          - Time window for calculating PERCLOS percentage
          - Longer periods = more stable readings
          - Shorter periods = faster response
          - Default: 60 seconds
        
        ### Drowsiness States:
        
        - **Awake**: Eyes are open most of the time
        - **Semi-Closed**: Eyes are closing more frequently
        - **Moderately Drowsy**: Significant eye closure, early drowsiness
        - **Drowsy**: High level of drowsiness, break recommended
        - **Very Drowsy**: Extreme drowsiness, immediate action required
        - **Sleeping**: Eyes closed continuously or PERCLOS above threshold
        
        ### Audio Alerts:
        
        The system plays audio alerts when drowsiness is detected:
        - Each alert plays once per PERCLOS period
        - Alerts escalate based on drowsiness level
        - Sleeping alert can play multiple times
        """)


if __name__ == "__main__":
    create_config_page()
