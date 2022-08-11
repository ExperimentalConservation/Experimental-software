import numpy as np


# Function that removes all widgets (and their index) from a PyQt layout
def clearPyQtLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearPyQtLayout(item.layout())


# Function to calculate the intersection over union value of two boxes
def compute_iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


# Function to calculate midpoint between two points
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# Function to remove Boxes that overlap with other Boxes (specifying the IOU)
def delOverlapBox(detection_params, MaxOverlapBBoxIOU):
    detection_params_NOL = []  # new list storing the non-overlapping detections
    if len(detection_params) == 1:  # if there is only one detection, we append it
        for detection in detection_params:
            detection_params_NOL.append(detection)
    if len(detection_params) > 1:  # if there are at least 2 detections, we check if their Bbox do not overlap
        for detection in detection_params:
            OtherDetections = [detections for detections in detection_params if (detections != detection)]  # all the other bounding boxes against which we want to test the overlap
            iou = 0
            for otherdetection in OtherDetections:
                Bbox1 = [detection[20], detection[21], detection[22], detection[23]]
                Bbox2 = [otherdetection[20], otherdetection[21], otherdetection[22], otherdetection[23]]
                iou = max(iou, compute_iou(Bbox1, Bbox2))  # if compute_iou gives 0 then there is no overlap
            if iou <= MaxOverlapBBoxIOU:
                detection_params_NOL.append(detection)
    return detection_params_NOL

# Function to calculate the distances between one point and all the points in a list
def distance(point, liste_points):
    distances = []
    for p in liste_points:
        distances.append(np.sum(np.power(p - np.expand_dims(point, axis=-1), 2)))
    return distances