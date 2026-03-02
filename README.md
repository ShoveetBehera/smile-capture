<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5dc8d3a8158c3535ed9ebacf1e586274d3042966
# Smile Capture 

So basically this project captures a photo of you automatically when you smile — no button pressing, nothing. Just open it, sit in front of your camera, and smile. It saves the photo on its own.

I made this to learn how OpenCV works and get comfortable with real-time video and face detection. Turned out pretty cool honestly.

---

## The idea

I wanted to do something more interesting than the usual "display webcam feed" tutorial. The smile detection part was tricky to get right — at first it was triggering on literally everything, so I added a consecutive frame check which helped a lot. Now it only captures when you actually hold a smile for a second.

---

## How to run it

```bash
git clone https://github.com/YOUR_USERNAME/smile-capture.git
cd smile-capture
pip install -r requirements.txt
python smile_capture.py
```

Smile at the camera, photo gets saved in `captured_photos/`. Press Q when you're done.

---

## Folder structure

```
smile-capture/
├── smile_capture.py       
├── captured_photos/       
├── requirements.txt       
└── README.md              
```

---

## How it actually works

OpenCV has these pre-trained models called Haar Cascades that can detect faces and smiles in images. The script grabs each frame from your webcam, converts it to grayscale, finds your face, then looks specifically at the lower half of the face (so it's not wasting time checking your forehead for a smile).

If it finds a smile consistently across a few frames, it saves the photo. There's also a cooldown so it doesn't save 15 copies in one second.

No extra downloads needed — the cascade files come bundled with OpenCV itself.

---

## Stuff I ran into

Getting the smile detection sensitivity right took some trial and error. Too sensitive and it fires on everything, not sensitive enough and it never triggers. The `minNeighbors` parameter in OpenCV controls this — higher value means stricter detection.

Lighting also matters way more than I expected. Works best when your face is well lit and you're facing the camera straight on.

---

## Requirements

- Python 3
- opencv-python

---

## If something's not working

Camera not opening — something else is probably using it (Zoom, browser, etc). Close those and try again, or change `VideoCapture(0)` to `VideoCapture(1)` in the script.

Smile not detecting — more light, face the camera directly, hold the smile for a moment instead of a quick flash.
=======
# SMILE-CAPTURE
>>>>>>> 1452191d4f24519fb5207645beb1b5284bdc3011

