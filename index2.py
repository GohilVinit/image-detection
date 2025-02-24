import cv2

# Load the pre-trained model and classes
classNames = []
classFile = 'coco_dataset.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'
    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    # Read frame from the camera
    success,img = cap.read()
    if not success:
        print("Failed to read from camera.")
        break

    # Detect objects in the frame
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classIds, bbox)

    # Draw bounding boxes and labels
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId-1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Display the output frame
    cv2.imshow("Output", img)

    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
