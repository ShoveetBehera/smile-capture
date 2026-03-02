import cv2
import os
import time

SAVE_DIR = "captured_photos"
SMILE_FRAMES_NEEDED = 5
COOLDOWN_SECONDS = 3

os.makedirs(SAVE_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

smile_counter = 0
last_capture_time = 0
photo_count = 0

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(80, 80)
    )

    smile_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 200, 0), 2)

        roi_gray = gray[y + h//2 : y + h, x : x + w]
        roi_color = frame[y + h//2 : y + h, x : x + w]

        smiles = smile_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25)
        )

        if len(smiles) > 0:
            smile_detected = True
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 100), 2)

        eye_roi_gray = gray[y:y + h//2, x:x + w]
        eye_roi_color = frame[y:y + h//2, x:x + w]

        eyes = eye_cascade.detectMultiScale(
            eye_roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20)
        )

        eyes = sorted(eyes, key=lambda e: e[0])

        for i, (ex, ey, ew, eh) in enumerate(eyes[:2]):

            if len(eyes) >= 2:
                eye_label = "Right Eye" if i == 0 else "Left Eye"
            else:
                eye_label = "Eye"

            cv2.rectangle(eye_roi_color, (ex, ey), (ex + ew, ey + eh), (0, 200, 255), 2)

            cv2.putText(frame, eye_label,
                        (x + ex, y + ey - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)

            pupil_roi = eye_roi_gray[ey:ey + eh, ex:ex + ew]
            _, threshold = cv2.threshold(pupil_roi, 50, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    px = int(M["m10"] / M["m00"])
                    if px < ew // 2:
                        gaze = "Looking Left"
                    else:
                        gaze = "Looking Right"

                    gaze_y = y - 30 if i == 0 else y - 50
                    cv2.putText(frame, f"{eye_label}: {gaze}",
                                (x, gaze_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)

        label = "Smiling" if smile_detected else "No Smile"
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 100) if smile_detected else (100, 100, 255), 2)

    current_time = time.time()
    cooldown_passed = (current_time - last_capture_time) > COOLDOWN_SECONDS

    if smile_detected:
        smile_counter += 1
    else:
        smile_counter = 0

    if smile_counter >= SMILE_FRAMES_NEEDED and cooldown_passed:
        photo_count += 1
        filename = os.path.join(SAVE_DIR, f"smile_{photo_count:03d}.jpg")
        cv2.imwrite(filename, frame)
        last_capture_time = current_time
        smile_counter = 0
        print(f"Photo saved: {filename}")

    cv2.putText(frame, f"Photos: {photo_count}", (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Smile + Gaze Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()