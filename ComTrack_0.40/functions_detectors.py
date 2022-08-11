import cv2 # OpenCV
import numpy as np # NumPy
from scipy.spatial import distance
from imutils import perspective

from functions_misc import midpoint, delOverlapBox

def detectSOBBandCSRT(framenumber, frame, detectionParams, outputParams, arenaCoords, trackerCSRT, objectBBCoords):
    firstTrackingFrame = outputParams["outputStartFrame"]
    detections = []
    detection = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,""]
    # If it's the first frame of the tracking, we need to load it into the tracker and init the tracker
    if framenumber == firstTrackingFrame:
        trackerCSRT.init(frame, objectBBCoords)
        bBox_XTopLeft = objectBBCoords[0]
        bBox_YTopLeft = objectBBCoords[1]
        bBox_XBottomRight = objectBBCoords[0] + objectBBCoords[2]
        bBox_YBottomRight = objectBBCoords[1] + objectBBCoords[3]
        width = objectBBCoords[2]
        height = objectBBCoords[3]
    # If it's not the first frame, we update the tracker with the new frame
    else:
        success, box = trackerCSRT.update(frame)  #maybe frameCopy?
        if success:
            [xTopLeft, yTopLeft, width, height] = [int(v) for v in box]

            bBox_XTopLeft = xTopLeft
            bBox_YTopLeft = yTopLeft
            bBox_XBottomRight = xTopLeft + width
            bBox_YBottomRight = yTopLeft + height
        else:
            bBox_XTopLeft = 0
            bBox_YTopLeft = 0
            bBox_XBottomRight = 0
            bBox_YBottomRight = 0
            width = 0
            height = 0

    object_width = min(width, height)
    object_length = max(width, height)
    object_centerX = bBox_XTopLeft + (width/2)
    object_centerY = bBox_YTopLeft + (height/2)

    # Coordinates of the LARGE bounding box of the detection (X px around the bounding box)
    if (detectionParams["detectionFeaturesEnlargeBBoxes"] == True):
        lBbox_Xtopleft = max(0, bBox_XTopLeft - detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
        lBbox_Ytopleft = max(0, bBox_YTopLeft - detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
        lBbox_Xbottomright = min(frame.shape[1], bBox_XBottomRight + detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
        lBbox_Ybottomright = min(frame.shape[0], bBox_YBottomRight + detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
    else:
        lBbox_Xtopleft = bBox_XTopLeft
        lBbox_Ytopleft = bBox_YTopLeft
        lBbox_Xbottomright = bBox_XBottomRight
        lBbox_Ybottomright = bBox_YBottomRight

    # Replacing detection value by the calculating values
    detection[0] = int(object_centerX)
    detection[1] = int(object_centerY)
    detection[2] = round(object_width, 3)
    detection[3] = round(object_length, 3)
    detection[6] = int(bBox_XTopLeft)
    detection[7] = int(bBox_YTopLeft)
    detection[8] = int(bBox_XBottomRight)
    detection[9] = int(bBox_YBottomRight)
    detection[10] = int(width)
    detection[11] = int(height)
    detection[20] = int(lBbox_Xtopleft)
    detection[21] = int(lBbox_Ytopleft)
    detection[22] = int(lBbox_Xbottomright)
    detection[23] = int(lBbox_Ybottomright)

    # Only consider detections that are not touching the borders of either the whole frame or the specified arena
    if arenaCoords == [0, 0, 0, 0]:
        if lBbox_Xtopleft > 0 and lBbox_Ytopleft > 0 and lBbox_Xbottomright < frame.shape[1] and lBbox_Ybottomright < frame.shape[0]:
            detections.append(detection)
    else:
        if lBbox_Xtopleft > arenaCoords[0] and lBbox_Ytopleft > arenaCoords[1] and lBbox_Xbottomright < arenaCoords[0] + arenaCoords[2] and lBbox_Ybottomright < arenaCoords[1] + arenaCoords[3]:
            detections.append(detection)

    return detections, trackerCSRT


def detectBSubAndThresh(frame, detectionParams, backSub, framenumber, startingFramenumber, arenaCoords):

    # prepare the target image
    target = np.zeros(shape=frame.shape, dtype=np.uint8)
    target.fill(0)
    # prepare the mask
    mask = np.zeros(shape=frame.shape, dtype=np.uint8)
    mask.fill(0)

    detections = []
    sortedDetections = []
    proceedFrame = False

    if detectionParams["selectDetectionMethod"] == "Thresholding":
        if detectionParams["detectionMethodThresh_Type"] == 'THRESH_BINARY': Type = cv2.THRESH_BINARY
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_BINARY_INV': Type = cv2.THRESH_BINARY_INV
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_TRUNC': Type = cv2.THRESH_TRUNC
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_TOZERO': Type = cv2.THRESH_TOZERO
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_TOZERO_INV': Type = cv2.THRESH_TOZERO_INV
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_MASK': Type = cv2.THRESH_MASK
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_OTSU': Type = cv2.THRESH_OTSU
        elif detectionParams["detectionMethodThresh_Type"] == 'THRESH_TRIANGLE': Type = cv2.THRESH_TRIANGLE
        newFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, newFrame = cv2.threshold(src=newFrame, thresh=detectionParams["detectionMethodThresh_ThreshVal"], maxval=detectionParams["detectionMethodThresh_MaxVal"], type=Type)
        proceedFrame = True
    elif detectionParams["selectDetectionMethod"] == "Background Subtraction":
        if detectionParams["detectionMethodBackSub_BackSubMethod"] != "None":
            newFrame = backSub.apply(frame)
            if detectionParams["detectionMethodBackSub_BackSubMethod"] == "KNN":
                if framenumber >= startingFramenumber + detectionParams["backgroundSubtractionMethodKNNHistory"]:
                    proceedFrame = True

    if proceedFrame is True:
        if detectionParams["contoursDetectionMethod"] == "CHAIN_APPROX_SIMPLE": CDMethod = cv2.CHAIN_APPROX_SIMPLE
        elif detectionParams["contoursDetectionMethod"] == "CHAIN_APPROX_NONE": CDMethod = cv2.CHAIN_APPROX_NONE

        if detectionParams["contoursDetectionMode"] == "RETR_EXTERNAL": CDMode = cv2.RETR_EXTERNAL
        elif detectionParams["contoursDetectionMode"] == "RETR_TREE": CDMode = cv2.RETR_TREE
        elif detectionParams["contoursDetectionMode"] == "RETR_LIST": CDMode = cv2.RETR_LIST
        elif detectionParams["contoursDetectionMode"] == "RETR_CCOMP": CDMode = cv2.RETR_CCOMP
        
        contours, hierarchy = cv2.findContours(image=newFrame, mode=CDMode, method=CDMethod)
        if len(contours) > 0:
            for cnt in contours:
                if cv2.contourArea(cnt) > detectionParams["contoursDetectionMinArea"] and cv2.contourArea(cnt) < detectionParams["contoursDetectionMaxArea"]:
                    # Surface area of the detection
                    object_area = cv2.contourArea(cnt)

                    # Centroid of the detection
                    Moment = cv2.moments(cnt)
                    object_centerX = int(Moment["m10"] / Moment["m00"])
                    object_centerY = int(Moment["m01"] / Moment["m00"])

                    # Coordinates of the bounding box of the detection
                    (Bbox_Xtopleft, Bbox_Ytopleft, Bbox_Width, Bbox_Height) = cv2.boundingRect(cnt)
                    Bbox_Xbottomright = Bbox_Xtopleft + Bbox_Width
                    Bbox_Ybottomright = Bbox_Ytopleft + Bbox_Height

                    # Coordinates of the LARGE bounding box of the detection (X px around the bounding box)
                    if (detectionParams["detectionFeaturesEnlargeBBoxes"] == True):
                        lBbox_Xtopleft = max(0, Bbox_Xtopleft - detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
                        lBbox_Ytopleft = max(0, Bbox_Ytopleft - detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
                        lBbox_Xbottomright = min(frame.shape[1], Bbox_Xbottomright + detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
                        lBbox_Ybottomright = min(frame.shape[0], Bbox_Ybottomright + detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
                    else:
                        lBbox_Xtopleft = Bbox_Xtopleft
                        lBbox_Ytopleft = Bbox_Ytopleft
                        lBbox_Xbottomright = Bbox_Xbottomright
                        lBbox_Ybottomright = Bbox_Ybottomright

                    # Coordinates of the rotated bounding box of the detection
                    rotbRect = cv2.minAreaRect(cnt)
                    rotbRectBox = cv2.boxPoints(rotbRect)
                    rotbRectBox = np.int0(rotbRectBox)
                    rotbRectBox = perspective.order_points(rotbRectBox)  # order points that way: top left, top right, bottom right, bottom left
                    (rBbox_TopleftPt, rBbox_ToprightPt, rBbox_BottomrightPt, rBbox_BottomleftPt) = rotbRectBox

                    # Angle of the rotated bounding box of the detection
                    object_angle = rotbRect[2]

                    # Coordinates of the midpoint between the top-left and top-right points of the rotated bounding box
                    (TopMidPt_X, TopMidPt_Y) = midpoint(rBbox_TopleftPt, rBbox_ToprightPt)

                    # Coordinates of the midpoint between the bottom-left and bottom-right points of the rotated bounding box
                    (BottomMidPt_X, BottomMidPt_Y) = midpoint(rBbox_BottomleftPt, rBbox_BottomrightPt)

                    # Coordinates of the midpoint between the top-left and bottom-left points of the rotated bounding box
                    (LeftMidPt_X, LeftMidPt_Y) = midpoint(rBbox_TopleftPt, rBbox_BottomleftPt)

                    # Coordinates of the midpoint between the top-right and bottom-right points of the rotated bounding box
                    (RightMidPt_X, RightMidPt_Y) = midpoint(rBbox_ToprightPt, rBbox_BottomrightPt)

                    # Compute the Euclidean distance between the midpoints
                    distance_TopBottom = distance.euclidean((TopMidPt_X, TopMidPt_Y), (BottomMidPt_X, BottomMidPt_Y))
                    distance_LeftRight = distance.euclidean((LeftMidPt_X, LeftMidPt_Y), (RightMidPt_X, RightMidPt_Y))

                    # Width and length of the detection (i.e. of the rotated bounding box)
                    object_width = min(distance_TopBottom, distance_LeftRight)
                    object_length = max(distance_TopBottom, distance_LeftRight)

                    # Reshape contour coordinates
                    cntCoordX = [x[0][0] for x in cnt]
                    cntCoordY = [x[0][1] for x in cnt]

                    detection = [
                        int(object_centerX),  # Param 0
                        int(object_centerY),  # Param 1
                        round(object_width, 3),  # Param 2
                        round(object_length, 3),  # Param 3
                        round(object_area, 3),  # Param 4
                        round(object_angle, 3),  # Param 5
                        int(Bbox_Xtopleft),  # Param 6
                        int(Bbox_Ytopleft),  # Param 7
                        int(Bbox_Xbottomright),  # Param 8
                        int(Bbox_Ybottomright),  # Param 9
                        int(Bbox_Width),  # Param 10
                        int(Bbox_Height),  # Param 11
                        int(rBbox_TopleftPt[0]),  # Param 12
                        int(rBbox_TopleftPt[1]),  # Param 13
                        int(rBbox_ToprightPt[0]),  # Param 14
                        int(rBbox_ToprightPt[1]),  # Param 15
                        int(rBbox_BottomrightPt[0]),  # Param 16
                        int(rBbox_BottomrightPt[1]),  # Param 17
                        int(rBbox_BottomleftPt[0]),  # Param 18
                        int(rBbox_BottomleftPt[1]),  # Param 19
                        int(lBbox_Xtopleft),  # Param 20
                        int(lBbox_Ytopleft),  # Param 21
                        int(lBbox_Xbottomright),  # Param 22
                        int(lBbox_Ybottomright),  # Param 23
                        cntCoordX,  # Param 24
                        cntCoordY,  # Param 25
                        cnt  # Param 26
                    ]

                    # Only consider detections that are not touching the borders of either the whole frame or the specified arena
                    if arenaCoords == [0, 0, 0, 0]:
                        if lBbox_Xtopleft > 0 and lBbox_Ytopleft > 0 and lBbox_Xbottomright < frame.shape[1] and lBbox_Ybottomright < frame.shape[0]:
                            detections.append(detection)
                    else:
                        if lBbox_Xtopleft > arenaCoords[0] and lBbox_Ytopleft > arenaCoords[1] and lBbox_Xbottomright < arenaCoords[0] + arenaCoords[2] and lBbox_Ybottomright < arenaCoords[1] + arenaCoords[3]:
                            detections.append(detection)


        # Find the bounding boxes that do not overlap with one another
        if (detectionParams["detectionFeaturesIgnoreOverlappingBBoxes"] == False):
            overlappingDetections = detections
            for detection in overlappingDetections:
                if detectionParams["detectionFeaturesRemoveBG"] is True:
                    cv2.drawContours(image=mask, contours=[detection[26]], contourIdx=0, color=(255, 255, 255), thickness=-1)
                # we then remove the contour element from the detection list
                # del detection[-1]
                sortedDetections.append(detection)
        else:
            if len(detections) > 0:
                noOverlappingDetections = delOverlapBox(detections, detectionParams["detectionFeaturesIgnoreOverlappingBBoxesEntry"])
                for detection in noOverlappingDetections:
                    if detectionParams["detectionFeaturesRemoveBG"] is True:
                        cv2.drawContours(image=mask, contours=[detection[26]], contourIdx=0, color=(255, 255, 255), thickness=-1)
                    # we then remove the contour element from the detection list
                    # del detection[-1]
                    sortedDetections.append(detection)
        
        if detectionParams["detectionFeaturesRemoveBG"] is True:
            # create image containing only what's inside the selected contours
            target = cv2.bitwise_and(src1=frame, src2=mask, mask=None)
        else:
            target = frame

    return sortedDetections, target
