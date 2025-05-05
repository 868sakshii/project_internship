import streamlit as st
import threading
import time
from src.audio_transcription import transcribe_audio
from src.keyword_detection import KeywordDetector
import os

# Define known contacts
KNOWN_CONTACTS = {
    "1234567890": "John Doe",
    "9876543210": "Jane Smith",
    "4567891230": "Alice Johnson",
    "3214569870": "Bob Brown",
}

def is_unknown_number(caller_number):
    """
    Check if the incoming number is unknown.
    """
    return caller_number not in KNOWN_CONTACTS

def risk_assessment(transcription, detector):
    """
    Perform risk assessment on the transcription using the KeywordDetector.
    """
    try:
        detection_result = detector.detect_keywords(transcription)
        return detection_result
    except Exception as e:
        st.error(f"Error during risk assessment: {e}")
        return None

def audio_processing(detector):
    """
    Simulate audio transcription and risk assessment.
    """
    try:
        transcription = transcribe_audio()
        return transcription, risk_assessment(transcription, detector)
    except Exception as e:
        st.error(f"Error during audio processing: {e}")
        return None, None

def main():
    """
    Streamlit app for scam call detection.
    """
    st.set_page_config(page_title="Scam Call Detection System", layout="wide")

    # Title and description
    st.title("📞 Scam Call Detection System")
    st.markdown("Identify potential scam calls in real-time using audio transcription and keyword detection.")

    # Sidebar for user input
    with st.sidebar:
        st.header("Settings")
        caller_number = st.text_input("Enter Caller Number", value="9998887776")
        scam_threshold = st.slider("Set Scam Threshold", 0.1, 1.0, 0.4, 0.1)
        st.markdown("---")
        st.info("Customize the system settings using this panel.")

    # Display caller information
    st.subheader("📇 Caller Details")
    col1, col2 = st.columns([1, 2])

    with col1:
        if is_unknown_number(caller_number):
            st.error(f"Unknown Caller: {caller_number}")
        else:
            st.success(f"Known Caller: {KNOWN_CONTACTS[caller_number]} ({caller_number})")

    with col2:
        st.write("*Scam Detection in Progress...*")

        # Initialize KeywordDetector
        model_path = "D:\\scam-call-detection\\saved_model"
        if not os.path.exists(model_path):
            st.error(f"Model path does not exist: {model_path}")
            return

        try:
            detector = KeywordDetector(model_path=model_path, scam_threshold=scam_threshold)
        except Exception as e:
            st.error(f"Error initializing KeywordDetector: {e}")
            return

        # Start transcription and risk assessment
        if st.button("Start Audio Analysis"):
            transcription, detection_result = audio_processing(detector)

            if transcription:
                st.write(f"*Transcription:* {transcription}")

                if detection_result and detection_result["is_scam"]:
                    st.warning(f"⚠ Scam Alert! Confidence: {detection_result['confidence']:.2f}")
                elif detection_result:
                    st.success(f"✔ Safe: Confidence: {detection_result['confidence']:.2f}")
                else:
                    st.info("No scam keywords detected.")
            else:
                st.error("No transcription detected.")

    # Footer
    st.markdown("---")
    st.markdown("Developed by Your Name | Real-Time Scam Detection System | 2024")

if __name__ == "_main_":
    main()
