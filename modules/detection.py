import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import time
import numpy as np
import winsound

from tensorflow.keras.models import load_model
from modules.database import connect

# LOAD AI MODEL
MODEL_PATH = "model/mask_detector.keras"

model = load_model(MODEL_PATH)

# FACE DETECTOR
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# CONFIG
IMG_SIZE = 224

CONFIDENCE_THRESHOLD = 0.55

ALERT_INTERVAL = 10

SAVE_FOLDER = "static/uploads"

last_alert_time = 0
live_face_count = 0
live_violation_count = 0


# PREDICT FACE
def predict_face(face):

    img = cv2.resize(face, (IMG_SIZE, IMG_SIZE))

    img = img.astype("float32") / 255.0

    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img, verbose=0)[0]

    mask_score = float(prediction[0])

    no_mask_score = float(prediction[1])

    if mask_score > no_mask_score:

        return "Mask", mask_score

    return "No Mask", no_mask_score


# SAVE VIOLATION
def save_violation(frame, confidence):

    timestamp = int(time.time())

    filename = f"{SAVE_FOLDER}/violation_{timestamp}.jpg"

    cv2.imwrite(filename, frame)

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO violations(image, result, confidence)
        VALUES (?, ?, ?)
    """, (
        filename,
        "No Mask",
        round(confidence, 2)
    ))

    conn.commit()

    conn.close()

    print(f"[INFO] Violation saved: {filename}")

    return filename


# PLAY ALERT
def play_alert():

    try:

        winsound.PlaySound(
            "static/sounds/alert.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

    except Exception as e:

        print("Alert sound error:", e)


# DRAW TOP UI
def draw_ui(frame, fps, total_faces):

    # TOP BAR
    cv2.rectangle(frame, (0, 0), (500, 90), (0, 0, 0), -1)

    # TITLE
    cv2.putText(
        frame,
        "iDetector - Real AI Monitoring",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    # FPS
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # FACE COUNT
    cv2.putText(
        frame,
        f"Faces: {total_faces}",
        (180, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    return frame


# GENERATE VIDEO FRAMES
def generate_frames():

    global last_alert_time
    global live_face_count
    global live_violation_count

    # CAMERA
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():

        print("[ERROR] Camera not detected")

        return

    prev_time = 0

    while True:

        success, frame = cap.read()

        if not success:

            break

        # FPS CALCULATION
        current_time = time.time()

        fps = int(1 / (current_time - prev_time + 0.0001))

        prev_time = current_time

        # FACE DETECTION
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # UPDATE LIVE FACE COUNT
        live_face_count = len(faces)

        # PROCESS EACH FACE
        for (x, y, w, h) in faces:

            # FACE CROP
            face = frame[y:y+h, x:x+w]

            # AI PREDICTION
            result, confidence = predict_face(face)

            # TERMINAL LOG
            print(f"[DETECTION] {result} | Confidence: {confidence:.2f}")

            # COLORS
            if result == "Mask":

                color = (0, 255, 0)

            else:

                color = (0, 0, 255)

                # SAVE ONLY HIGH CONFIDENCE
                if confidence >= CONFIDENCE_THRESHOLD:

                    # PREVENT MULTIPLE ALERTS
                    if current_time - last_alert_time > ALERT_INTERVAL:

                        play_alert()

                        save_violation(frame, confidence)

                        last_alert_time = current_time

                        # UPDATE VIOLATION COUNT
                        live_violation_count += 1

            # DRAW FACE BOX
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

            # DRAW LABEL
            cv2.putText(
                frame,
                f"{result}: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        # DRAW UI
        frame = draw_ui(
            frame,
            fps,
            live_face_count
        )

        # ENCODE FRAME
        ret, buffer = cv2.imencode(".jpg", frame)

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

    # RELEASE CAMERA
    cap.release()

    cv2.destroyAllWindows()