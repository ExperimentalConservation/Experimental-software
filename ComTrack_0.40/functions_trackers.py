import numpy as np

from functions_misc import compute_iou, distance

def trackSOBBandCSRT(framenumber, detections, outputData, detectionParams, trackingParams, outputParams):
    label = detectionParams["detectionFeaturesPreLabelDetectionsEntry"]
    outputDataCondition = outputParams["outputExportData"]
    outputDataFilePath = outputParams["outputDataFile"]
    

    outputData_frame = []  # this is where we'll store all the data for this specific video frame

    for detection in detections:
        contour = detection[24]
        storage_temp = [framenumber, 0]  # Only one detection for SOOB and CSRT method, so only ID "1" in the tracked object
        storage_temp.extend(detection)
        storage_temp.insert(len(storage_temp), contour)
        storage_temp.insert(len(storage_temp), label)
        outputData_frame.append(storage_temp)
    # We add each detection of this frame in the big storage dataframe
    if (outputDataCondition is True) & (outputDataFilePath != "None"):
        for detection in outputData_frame:
            outputData.loc[len(outputData)] = detection
    return outputData, outputData_frame


def trackKalmanFilter(framenumber, frame, detections, objets_points, objets_KF, object_IDs, id_objet, outputData, detectionParams, trackingParams, outputParams):
    noiseKF = trackingParams["trackingMethodKalmanFilterParametersNoise"]
    timeKF = trackingParams["trackingMethodKalmanFilterParametersTimeStep"]
    distKF = trackingParams["trackingMethodKalmanFilterParametersMaxDistance"]
    label = detectionParams["detectionFeaturesPreLabelDetectionsEntry"]
    
    outputDataCondition = outputParams["outputExportData"]
    outputDataFilePath = outputParams["outputDataFile"]
    # Predict locations from the detections of the previous frame
    for id_obj in range(len(objets_points)):
        etat = objets_KF[id_obj].predict()  # run KF predictions on the objects from the previous frame
        etat = np.array(etat, dtype=np.int32)
        objets_points[id_obj] = np.array([etat[0], etat[1], etat[4], etat[5]])  # objets_points is now filled with the info from the KF prediction
    
    # Calculating distances between KF predictions and detections, and associating detection to a KF filter
    points = [filter[0:4] for filter in detections]

    # We create a vector full of 1 of length equal to the number of detected objects
    # We'll give to each row of this nouveaux_objets the value of 0 if the detected object has a KF filter
    # (i.e. object already detected and identified in previous frame)
    # We'll leave the value to 1 if not, to build a new KF filter for this new object
    nouveaux_objets = np.ones((len(points)))

    # Initialisation of vectors/arrays related to the frame
    tab_distances = []  # this is where we'll store the distances between KF predictions and detections
    outputData_frame = []  # this is where we'll store all the data for this specific video frame

    if len(objets_points):  # we only operate this is there are KF filters (i.e. if detections and subsequent building of new KF filter were made in the previous frame)
        for point_id in range(len(points)):
            distances = distance(points[point_id], objets_points)
            tab_distances.append(distances)

        tab_distances = np.array(tab_distances)
        sorted_distances = np.sort(tab_distances, axis=None)  # sorting the distances (smallest to largest)

        for d in sorted_distances:
            if d > distKF:
                break  # if distance is > to distance_maxi (a parameter set up initially) then the new detection can't be associated to a KF filter from the previous frame, so break, and we leave nouveaux_objets value to 1 to create a KF filter for this detection
            id1, id2 = np.where(tab_distances == d)
            # if distance < distance_maxi, then we look in points and objets_points which detection (id1) and filter (id2) can be associated
            if not len(id1) or not len(id2):
                continue  # if there is no id1 nor id2, it means there is no association possible between the detection and a KF filter already existing, then we leave nouveaux_objets to 1 to build a new KF filter for this detection
            # if there is an id1 and an id2 then we perform the following:
            tab_distances[id1, :] = distKF + 1  # we put the distance above distance maxi, it's a way to say: we'll not look at this anymore because we have found what we were looking for
            tab_distances[:, id2] = distKF + 1
            for i in range(len(id1)):
                objets_KF[id2[i]].update(np.expand_dims(points[id1[i]], axis=-1))  # I'm not sure but I think this update the KF filter with the id id2, with the new detection id1 of this object made by the detector
                storage_temp = [framenumber, object_IDs[id2[i]]]
                storage_temp.extend(detections[id1[i]])
                storage_temp.insert(len(storage_temp), label)
                outputData_frame.append(storage_temp)
            nouveaux_objets[id1] = 0  # we put the value 0 so that we don't build a new KF filter for this object (see below)

    # Creating new KF filter for new objects
    for point_id in range(len(points)):
        if nouveaux_objets[point_id]:  # here you can see that we only do this for objects that have ones in nouveaux_objets (objects that were associated with a KF were given a value 0 for this, see above)
            objets_points.append(points[point_id])  # we put this new detection in the object list
            objets_KF.append(KalmanFilter(timeKF, [points[point_id][0], points[point_id][1]], [points[point_id][2], points[point_id][3]], noiseKF))  # we create a new KF for this new detection
            storage_temp = [framenumber, id_objet]
            storage_temp.extend(detections[point_id])
            storage_temp.insert(len(storage_temp), label)
            outputData_frame.append(storage_temp)
            object_IDs.append(id_objet)
            id_objet += 1
    
    # Suppressing objects that exit the window
    tab_id = []
    for id_point in range(len(objets_points)):
        if int(objets_points[id_point][0]) < 0 or int(objets_points[id_point][1]) < 0 or int(objets_points[id_point][0]) > frame.shape[1] or int(objets_points[id_point][1]) > frame.shape[0]:
            tab_id.append(id_point)
    for index in sorted(tab_id, reverse=True):
        del objets_points[index]
        del objets_KF[index]
        del object_IDs[index]

    # We add each detection of this frame in the big storage dataframe
    if (outputDataCondition is True) & (outputDataFilePath != "None"):
        for detection in outputData_frame:
            outputData.loc[len(outputData)] = detection
    
    return objets_points, objets_KF, object_IDs, id_objet, outputData, outputData_frame


class KalmanFilter(object):
    def __init__(self, dt, point, box, KFnoise):
        self.dt = dt

        # Vecteur d'etat initial
        self.E = np.matrix([[point[0]], [point[1]], [0], [0], [box[0]], [box[1]]])

        # Matrice de transition
        self.A = np.matrix([
            [1, 0, self.dt, 0, 0, 0],
            [0, 1, 0, self.dt, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])

        # Matrice d'observation, on observe x, y, width, height
        self.H = np.matrix([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])

        v = KFnoise
        # Matrice relative aux bruits
        self.Q = np.matrix([
            [v, 0, 0, 0, 0, 0],
            [0, v, 0, 0, 0, 0],
            [0, 0, v, 0, 0, 0],
            [0, 0, 0, v, 0, 0],
            [0, 0, 0, 0, v, 0],
            [0, 0, 0, 0, 0, v]
        ])

        # Matrice relative aux bruits de mesures
        self.R = np.matrix([
            [v, 0, 0, 0],
            [0, v, 0, 0],
            [0, 0, v, 0],
            [0, 0, 0, v]
        ])

        # Matrice autre
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        self.E = np.dot(self.A, self.E)
        # Calcul de la covariance de l'erreur
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.E

    def update(self, z):
        # Calcul du gain de Kalman
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Correction / innovation
        self.E = np.round(self.E + np.dot(K, (z - np.dot(self.H, self.E))))
        M = np.eye(self.H.shape[1])
        self.P = (M - (K * self.H)) * self.P

        return self.E
