# import os
# import threading
# from src.audio_transcription import transcribe_audio
# from src.keyword_detection import KeywordDetector  # Corrected import path
# import time

# # Initialize Keyword Detector with your fine-tuned model
# detector = KeywordDetector(model_path="D:\scam-call-detection\saved_model", scam_threshold=0.4)  # Adjust path and threshold as needed

# def risk_assessment(transcription):
#     """
#     Assess the risk of a transcription using the KeywordDetector.
#     """
#     detection_result = detector.detect_keywords(transcription)
    
#     # Print risk assessment results
#     print(f"Transcription: {transcription}")
#     if detection_result["is_scam"]:
#         print(f"⚠ Scam Alert: Confidence {detection_result['confidence']:.2f}")
#     else:
#         print(f"✔ Safe: Confidence {detection_result['confidence']:.2f}")
    
#     # Return the risk result for further processing
#     return detection_result


# def main():
#     """
#     Main function to integrate the entire workflow.
#     """
#     print("Starting real-time scam call detection system...\n")
    
#     # Launch audio transcription in a separate thread
#     def audio_processing():
#         print("Listening for audio...")
#         transcribe_audio()
    
#     try:
#         # Run audio transcription (with language detection) and risk assessment
#         threading.Thread(target=audio_processing, daemon=True).start()
        
#         while True:
#             # Simulate waiting for transcriptions to process (replace with your logic)
#             time.sleep(5)  # Adjust based on your processing speed

#     except KeyboardInterrupt:
#         print("\nExiting the scam call detection system.")
#     except Exception as e:
#         print(f"Error in main workflow: {e}")
#     finally:
#         print("System cleanup completed. Exiting.")

# if __name__ == "_main_":
#     main()



import os
import threading
from src.audio_transcription import transcribe_audio
from src.keyword_detection import KeywordDetector
import time

# Initialize Keyword Detector with your fine-tuned model
detector = KeywordDetector(model_path="E:\\scam_call_detection1.1\\saved_model", scam_threshold=0.4)  # Adjust path and threshold as needed

def risk_assessment(transcription):
    """
    Assess the risk of a transcription using the KeywordDetector.
    """
    detection_result = detector.detect_keywords(transcription)
    
    # Print risk assessment results
    print(f"Transcription: {transcription}")
    if detection_result["is_scam"]:
        print(f"⚠ Scam Alert: Confidence {detection_result['confidence']:.2f}")
    else:
        print(f"✔ Safe: Confidence {detection_result['confidence']:.2f}")
    
    # Return the risk result for further processing
    return detection_result

def audio_processing(transcriptions):
    """
    Continuously process audio and update the transcription list.
    """
    print("Listening for audio...")
    while True:
        # Replace with actual transcription logic
        transcription = transcribe_audio()
        if transcription:  # Add transcription to the shared list if valid
            transcriptions.append(transcription)

def main():
    """
    Main function to integrate the entire workflow.
    """
    print("Starting real-time scam call detection system...\n")
    transcriptions = []  # Shared list for storing transcriptions

    try:
        # Launch audio transcription in a separate thread
        threading.Thread(target=audio_processing, args=(transcriptions,), daemon=True).start()

        while True:
            # Check if there are any new transcriptions
            if transcriptions:
                transcription = transcriptions.pop(0)  # Process the oldest transcription
                risk_assessment(transcription)
            
            # Simulate waiting (adjust based on your processing speed)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting the scam call detection system.")
    except Exception as e:
        print(f"Error in main workflow: {e}")
    finally:
        print("System cleanup completed. Exiting.")

if __name__ == "__main__":
    main()
