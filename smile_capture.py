import cv2
import os
import time

SAVE_DIR = "captured_photos"
SMILE_FRAMES_NEEDED = 5     
COOLDOWN_SECONDS = 3         
\
os.makedirs(SAVE_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)


smile_counter = 0
last_capture_time = 0
photo_count = 0


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("✅ Smile Detection Started — Press Q to quit")


while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(80, 80)
    )

    smile_detected = False

    for (x, y, w, h) in faces:
     
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 200, 0), 2)

        roi_gray  = gray[y + h//2 : y + h, x : x + w]
        roi_color = frame[y + h//2 : y + h, x : x + w]

        smiles = smile_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25)
        )

        if len(smiles) > 0:
            smile_detected = True
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 100), 2)

        label = "😊 Smiling!" if smile_detected else "😐 No Smile"
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
        print(f"📸 Photo saved: {filename}")

        cv2.putText(frame, "📸 CAPTURED!", (50, 80),
                    cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 3)


    cv2.putText(frame, f"Photos taken: {photo_count}", (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Smile Capture 📸", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
print(f"✅ Done. {photo_count} photo(s) saved in '{SAVE_DIR}/'")