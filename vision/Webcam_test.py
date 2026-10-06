import cv2

camera=cv2.VideoCapture(0)

print(camera.isOpened())
while True:
    success, frame = camera.read()
       
    if not success:
        print("Could not capture a frame.")
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow("Webcam Test", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    

print(success)
camera.release()
cv2.destroyAllWindows()
