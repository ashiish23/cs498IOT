import os
import pathlib
import cv2
import argparse
import tensorflow as tf
import time
import numpy as np
import matplotlib.pyplot as plt
import warnings
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from threading import Thread

class VideoStream:
    def __init__(self,resolution=(640,480),framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

def start_stream(args):
    PATH_TO_MODEL_DIR = args.model
    PATH_TO_LABELS = args.labels
    MIN_CONF_THRESH = float(args.threshold)
    PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"

    start_time = time.time()
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Loading model took {} seconds'.format(elapsed_time))

    # Load label map data for plotting
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
    warnings.filterwarnings('ignore')

    print('Create stream for PiCamera')
    videostream = VideoStream(resolution=(640,480),framerate=30).start()
    
    while True:
        frame = videostream.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)
        imH, imW, _ = frame.shape

        input_tensor = tf.convert_to_tensor(frame)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = { key: value[0, :num_detections].numpy() for key, value in detections.items() }
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        scores = detections['detection_scores']
        boxes = detections['detection_boxes']
        classes = detections['detection_classes']
        count = 0

        for i in range(len(scores)):
            if ((scores[i] > MIN_CONF_THRESH) and (scores[i] <= 1.0)):
                count += 1
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                # Draw label
                object_name = category_index[int(classes[i])]['name']
                label = '%s: %d%%' % (object_name, int(scores[i]*100))
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) 
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
                

        cv2.putText (frame,'Objects Detected : ' + str(count),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(70,235,52),2,cv2.LINE_AA)
        cv2.imshow('Object Detector', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Use custom model, labels, or threshold if provided
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='saved model location', default='ssd_mobilenet_v2_320x320_coco17_tpu-8')
    parser.add_argument('--labels', help='labelmap location', default='models/research/object_detection/data/mscoco_label_map.pbtxt')
    parser.add_argument('--threshold', help='min confidence threshold for displaying detected objects', default=0.5)                    
    args = parser.parse_args()

    start_stream(args)