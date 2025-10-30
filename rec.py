import cv2

def capturePhoto():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Errore, non trovo la webcam")
    else:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("capture-photo/output.jpg", frame)
            print("Fatto")
        else:
            print("Errore leggendo il frame")

    cap.release()

capturePhoto()