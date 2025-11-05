import time
import pygame  # For playing audio
import os


class AttentionScorer:

    def __init__(self, t_now, ear_thresh=0, gaze_thresh=0, perclos_thresh=0.2, roll_thresh=60,
                 pitch_thresh=20, yaw_thresh=30, ear_time_thresh=4.0, gaze_time_thresh=2.,
                 pose_time_thresh=4.0, verbose=False):
        self.ear_thresh = ear_thresh
        self.gaze_thresh = gaze_thresh
        self.perclos_thresh = perclos_thresh
        self.roll_thresh = roll_thresh
        self.pitch_thresh = pitch_thresh
        self.yaw_thresh = yaw_thresh
        self.ear_time_thresh = ear_time_thresh
        self.gaze_time_thresh = gaze_time_thresh
        self.pose_time_thresh = pose_time_thresh
        self.verbose = verbose

        self.perclos_time_period = 60  # 60 seconds
        
        self.last_time_eye_opened = t_now
        self.last_time_looked_ahead = t_now
        self.last_time_attended = t_now
        self.closure_time = 0
        self.not_look_ahead_time = 0
        self.distracted_time = 0

        self.prev_time = t_now
        self.eye_closure_counter = 0
        
        # Add new variables for continuous closure tracking
        self.continuous_closure_start = None
        self.sleep_threshold = 3.0  # 3 seconds threshold
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Load audio files
        audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
        self.audio_files = {
            'Semi-Closed': os.path.join(audio_dir, 'Semi-closed.mp3'),
            'Moderately Drowsy': os.path.join(audio_dir, 'Moderate_Drowsiness.mp3'),
            'Drowsy': os.path.join(audio_dir, 'Drowsiness.mp3'),
            'Sleeping': os.path.join(audio_dir, 'Sleep.mp3')  # Use same sound for sleeping
        }
        
        # Track which alerts have been played this period
        self.alerts_played_this_period = set()


    def play_alert(self, alert_type):
        """Play alert sound once per condition per PERCLOS period"""
        # Only play if not awake and haven't played this specific alert this period yet
        if alert_type != 'Awake' and alert_type not in self.alerts_played_this_period and alert_type in self.audio_files:
            try:
                pygame.mixer.music.load(self.audio_files[alert_type])
                pygame.mixer.music.play()
                # If it is sleeping, dont mark other alerts as played
                if alert_type == 'Sleeping':
                    pass
                else:
                    self.alerts_played_this_period.add(alert_type)  # Mark this alert as played
                if self.verbose:
                    print(f"Playing alert: {alert_type}")
            except Exception as e:
                print(f"Error playing audio: {e}")


    def eval_scores(self, t_now, ear_score, gaze_score, head_roll, head_pitch, head_yaw):
        asleep = False
        looking_away = False
        distracted = False

        if self.closure_time >= self.ear_time_thresh:  # check if the ear cumulative counter surpassed the threshold
            asleep = True

        if self.not_look_ahead_time >= self.gaze_time_thresh:  # check if the gaze cumulative counter surpassed the threshold
            looking_away = True

        if self.distracted_time >= self.pose_time_thresh:  # check if the pose cumulative counter surpassed the threshold
            distracted = True

        if (ear_score is not None) and (ear_score <= self.ear_thresh):
            self.closure_time = t_now - self.last_time_eye_opened
        elif ear_score is None or (ear_score is not None and ear_score > self.ear_thresh):
            self.last_time_eye_opened = t_now
            self.closure_time = 0.

        if (gaze_score is not None) and (gaze_score > self.gaze_thresh):
            self.not_look_ahead_time = t_now - self.last_time_looked_ahead
        elif gaze_score is None or (gaze_score is not None and gaze_score <= self.gaze_thresh):
            self.last_time_looked_ahead = t_now
            self.not_look_ahead_time = 0.

        if ((head_roll is not None and abs(head_roll) > self.roll_thresh) or (
                head_pitch is not None and abs(head_pitch) > self.pitch_thresh) or (
                head_yaw is not None and abs(head_yaw) > self.yaw_thresh)):
            self.distracted_time = t_now - self.last_time_attended
        elif head_roll is None or head_pitch is None or head_yaw is None or (
            (abs(head_roll) <= self.roll_thresh) and (abs(head_pitch) <= self.pitch_thresh) and (
                abs(head_yaw) <= self.yaw_thresh)):
            self.last_time_attended = t_now
            self.distracted_time = 0.

        if self.verbose:  # print additional info if verbose is True
            print(
                f"ear counter:{self.ear_counter}/{self.ear_act_thresh}\ngaze counter:{self.gaze_counter}/{self.gaze_act_thresh}\npose counter:{self.pose_counter}/{self.pose_act_thresh}")
            print(
                f"eye closed:{asleep}\tlooking away:{looking_away}\tdistracted:{distracted}")

        return asleep, looking_away, distracted

    def get_PERCLOS(self, t_now, fps, ear_score):
        delta = t_now - self.prev_time  # set delta timer
        tired = ""  # set default value for the tired state of the driver

        all_frames_numbers_in_perclos_duration = int(self.perclos_time_period * fps)

        # Track continuous eye closure
        if (ear_score is not None) and (ear_score <= self.ear_thresh):
            if self.continuous_closure_start is None:
                self.continuous_closure_start = t_now
            
            # Check if eyes have been closed continuously for more than 3 seconds
            continuous_closure_time = t_now - self.continuous_closure_start
            if continuous_closure_time >= self.sleep_threshold:
                self.play_alert('Sleeping')
                return "Sleeping", 100.0  # Return immediately with sleeping status
            
            self.eye_closure_counter += 1
        else:
            # Eyes are open, reset continuous closure timer
            self.continuous_closure_start = None

        # compute the PERCLOS over a given time period
        perclos_score = (self.eye_closure_counter) / all_frames_numbers_in_perclos_duration
        
        # if perclos_score >= self.perclos_thresh:  # if the PERCLOS score is higher than a threshold, tired = True
        #     tired = True

        if perclos_score < 3.75:
            tired = "Awake"
        elif 3.75<perclos_score<=10:
            tired = "Semi-Closed"
        elif 10<perclos_score<=15:
            tired = "Moderately Drowsy"
        elif 15<perclos_score<=20:
            tired = "Drowsy"
        else:
            tired = "Sleeping"
        # Play appropriate alert based on drowsiness level (once per condition per period)
        self.play_alert(tired)

        if delta >= self.perclos_time_period:  # at every end of the given time period, reset the counter and the timer
            self.eye_closure_counter = 0
            self.prev_time = t_now
            self.alerts_played_this_period.clear()  # Clear all played alerts for new period
            print("=====================================")
            print("PERCLOS score reset")
            print("tired:", tired)
            print("perclos_score:", perclos_score)
            print("=====================================")

        return tired, perclos_score 