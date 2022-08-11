from bs4 import BeautifulSoup
import re

def getControlsAnnotations(imageSmoothingControlsWidget, detectionsControlsWidget, trackingControlsWidget):
    smoothingParams1 = {
            "smoothingActivated": False,
            "smoothingType": "None",
            "smoothingAverageBlurKernel": 1,
            "smoothingAverageBlurBorderType": "BORDER_DEFAULT",
            "smoothingMedianBlurKernel": 1,
            "smoothingGaussianBlurKernel": 1,
            "smoothingGaussianBlurSigmaX": 0,
            "smoothingGaussianBlurSigmaY": 0,
            "smoothingGaussianBlurBorderType": "BORDER_DEFAULT",
            "smoothingBilateralFilterFilterSize": 5,
            "smoothingBilateralFilterSigmaColor": 150,
            "smoothingBilateralFilterSigmaSpace": 150,
            "smoothingBilateralFilterBorderType": "BORDER_DEFAULT"
        }
    smoothingParams2 = smoothingParams1.copy()
    smoothingParams3 = smoothingParams1.copy()
    smoothingParams4 = smoothingParams1.copy()
    smoothingParams = [smoothingParams1, smoothingParams2, smoothingParams3, smoothingParams4]
    
    detectionParams = {
        "selectDetectionMethod": "None",
        "detectionMethodThresh_ThreshVal": 100,
        "detectionMethodThresh_MaxVal": 255,
        "detectionMethodThresh_Type": "THRESH_BINARY",
        "detectionMethodBackSub_BackSubMethod": "None",
        "backgroundSubtractionMethodKNNHistory": 20,
        "backgroundSubtractionMethodKNNThreshold": 2000,
        "backgroundSubtractionMethodKNNDetectShadows": False,
        "backgroundSubtractionMethodKNNShadowsValue": 127,
        "backgroundSubtractionMethodKNNShadowsThreshold": 0.5,
        "contoursDetectionMethod": "CHAIN_APPROX_SIMPLE",
        "contoursDetectionMode": "RETR_EXTERNAL",
        "contoursDetectionMinArea": 60,
        "contoursDetectionMaxArea": 5000,
        "detectionFeaturesPreLabelDetections": False,
        "detectionFeaturesPreLabelDetectionsEntry": "Species",
        "detectionFeaturesEnlargeBBoxes": False,
        "detectionFeaturesEnlargeBBoxesEntry": 25,
        "detectionFeaturesIgnoreOverlappingBBoxes": False,
        "detectionFeaturesIgnoreOverlappingBBoxesEntry": 0,
        "detectionFeaturesRemoveBG": False,
    }

    trackingParams = {
        "selectTrackingMethod": "None",
        "trackingMethodKalmanFilterParametersNoise": 1,
        "trackingMethodKalmanFilterParametersTimeStep": 0.01,
        "trackingMethodKalmanFilterParametersMaxDistance": 20000
    }

    index = 0
    for item in imageSmoothingControlsWidget.smoothingItemWidgets:
        try:
            smoothingmethod = item[1].smoothingItem.currentText()
            if smoothingmethod != "None":
                smoothingParams[index]["smoothingActivated"] = True
                smoothingParams[index]["smoothingType"] = item[1].smoothingItem.currentText()
                smoothingParams[index]["smoothingAverageBlurKernel"] = int(item[1].smoothingAverageBlurKernelEntry.value())
                smoothingParams[index]["smoothingAverageBlurBorderType"] = item[1].smoothingAverageBlurBorderTypeEntry.currentText()
                smoothingParams[index]["smoothingMedianBlurKernel"] = int(item[1].smoothingMedianBlurKernelEntry.value())
                smoothingParams[index]["smoothingGaussianBlurKernel"] = int(item[1].smoothingGaussianBlurKernelEntry.value())
                smoothingParams[index]["smoothingGaussianBlurSigmaX"] = round(item[1].smoothingGaussianBlurSigmaXEntry.value(), 3)
                smoothingParams[index]["smoothingGaussianBlurSigmaY"] = round(item[1].smoothingGaussianBlurSigmaYEntry.value(), 3)
                smoothingParams[index]["smoothingGaussianBlurBorderType"] = item[1].smoothingGaussianBlurBorderTypeEntry.currentText()
                smoothingParams[index]["smoothingBilateralFilterFilterSize"] = int(item[1].smoothingBilateralFilterFilterSizeEntry.value())
                smoothingParams[index]["smoothingBilateralFilterSigmaColor"] = int(item[1].smoothingBilateralFilterSigmaColorEntry.value())
                smoothingParams[index]["smoothingBilateralFilterSigmaSpace"] = int(item[1].smoothingBilateralFilterSigmaSpaceEntry.value())
                smoothingParams[index]["smoothingBilateralFilterBorderType"] = item[1].smoothingBilateralFilterBorderTypeEntry.currentText()
            index += 1
        except:
            return
    
    detectionParams["selectDetectionMethod"] = detectionsControlsWidget.selectDetectionMethod.currentText()
    detectionParams["detectionMethodThresh_ThreshVal"] = int(detectionsControlsWidget.detectionMethodThresh_ThreshVal.value())
    detectionParams["detectionMethodThresh_MaxVal"] = int(detectionsControlsWidget.detectionMethodThresh_MaxVal.value())
    detectionParams["detectionMethodThresh_Type"] = detectionsControlsWidget.detectionMethodThresh_Type.currentText()
    detectionParams["detectionMethodBackSub_BackSubMethod"] = detectionsControlsWidget.detectionMethodBackSub_BackSubMethod.currentText()
    detectionParams["backgroundSubtractionMethodKNNHistory"] = int(detectionsControlsWidget.backgroundSubtractionMethodKNNHistory.value())
    detectionParams["backgroundSubtractionMethodKNNThreshold"] = int(detectionsControlsWidget.backgroundSubtractionMethodKNNThreshold.value())
    detectionParams["backgroundSubtractionMethodKNNDetectShadows"] = detectionsControlsWidget.backgroundSubtractionMethodKNNDetectShadows.isChecked()
    detectionParams["backgroundSubtractionMethodKNNShadowsValue"] = int(detectionsControlsWidget.backgroundSubtractionMethodKNNShadowsValue.value())
    detectionParams["backgroundSubtractionMethodKNNShadowsThreshold"] = round(detectionsControlsWidget.backgroundSubtractionMethodKNNShadowsThreshold.value(), 2)
    detectionParams["contoursDetectionMethod"] = detectionsControlsWidget.contoursDetectionMethod.currentText()
    detectionParams["contoursDetectionMode"] = detectionsControlsWidget.contoursDetectionMode.currentText()
    detectionParams["contoursDetectionMinArea"] = int(detectionsControlsWidget.contoursDetectionMinArea.value())
    detectionParams["contoursDetectionMaxArea"] = int(detectionsControlsWidget.contoursDetectionMaxArea.value())
    detectionParams["detectionFeaturesPreLabelDetections"] = detectionsControlsWidget.detectionFeaturesPreLabelDetections.isChecked()
    detectionParams["detectionFeaturesPreLabelDetectionsEntry"] = detectionsControlsWidget.detectionFeaturesPreLabelDetectionsEntry.text()
    detectionParams["detectionFeaturesEnlargeBBoxes"] = detectionsControlsWidget.detectionFeaturesEnlargeBBoxes.isChecked()
    detectionParams["detectionFeaturesEnlargeBBoxesEntry"] = int(detectionsControlsWidget.detectionFeaturesEnlargeBBoxesEntry.value())
    detectionParams["detectionFeaturesIgnoreOverlappingBBoxes"] = detectionsControlsWidget.detectionFeaturesIgnoreOverlappingBBoxes.isChecked()
    detectionParams["detectionFeaturesIgnoreOverlappingBBoxesEntry"] = round(detectionsControlsWidget.detectionFeaturesIgnoreOverlappingBBoxesEntry.value(), 2)
    detectionParams["detectionFeaturesRemoveBG"] = detectionsControlsWidget.detectionFeaturesRemoveBG.isChecked()

    trackingParams["selectTrackingMethod"] = trackingControlsWidget.selectTrackingMethod.currentText()
    trackingParams["trackingMethodKalmanFilterParametersNoise"] = trackingControlsWidget.trackingMethodKalmanFilterParametersNoise.value()
    trackingParams["trackingMethodKalmanFilterParametersTimeStep"] = trackingControlsWidget.trackingMethodKalmanFilterParametersTimeStep.value()
    trackingParams["trackingMethodKalmanFilterParametersMaxDistance"] = trackingControlsWidget.trackingMethodKalmanFilterParametersMaxDistance.value()

    controlsAnnot = buildControlsAnnotations(smoothingParams, detectionParams, trackingParams)
    return controlsAnnot



def buildControlsAnnotations(smoothingParams, detectionParams, trackingParams):
    
    annotations = BeautifulSoup(features="lxml")

    # Annotations for Smoothing Params
    annot_smoothingParams = annotations.new_tag('SMOOTHING_PARAMS')
    annotations.append(annot_smoothingParams)
    for smoothingParam in smoothingParams:
        if (smoothingParam["smoothingType"] != "None"):
            annot_smoothingParams_Method = annotations.new_tag('Smoothing_Method')
            annot_smoothingParams.append(annot_smoothingParams_Method)

            annot_smoothingParams_smoothingName = annotations.new_tag('SmoothingName')
            annot_smoothingParams_smoothingName.string = str(smoothingParam["smoothingType"])
            annot_smoothingParams_Method.append(annot_smoothingParams_smoothingName)

            if (str(smoothingParam["smoothingType"]) == "Averaging"):
                annot_smoothingParams_Param_smoothingName_Averaging_Kernel = annotations.new_tag('AverageBlurKernel')
                annot_smoothingParams_Param_smoothingName_Averaging_Kernel.string = str(smoothingParam["smoothingAverageBlurKernel"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_Averaging_Kernel)

                annot_smoothingParams_Param_smoothingName_Averaging_BorderType = annotations.new_tag('AverageBlurBorderType')
                annot_smoothingParams_Param_smoothingName_Averaging_BorderType.string = str(smoothingParam["smoothingAverageBlurBorderType"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_Averaging_BorderType)

            elif (str(smoothingParam["smoothingType"]) == "Median Blurring"):
                annot_smoothingParams_Param_smoothingName_MedianBlurring_Kernel = annotations.new_tag('MedianBlurKernel')
                annot_smoothingParams_Param_smoothingName_MedianBlurring_Kernel.string = str(smoothingParam["smoothingMedianBlurKernel"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_MedianBlurring_Kernel)
            
            elif (str(smoothingParam["smoothingType"]) == "Gaussian Blurring"):
                annot_smoothingParams_Param_smoothingName_GaussianBlurring_Kernel = annotations.new_tag('GaussianBlurKernel')
                annot_smoothingParams_Param_smoothingName_GaussianBlurring_Kernel.string = str(smoothingParam["smoothingGaussianBlurKernel"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_GaussianBlurring_Kernel)

                annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaX = annotations.new_tag('GaussianBlurSigmaX')
                annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaX.string = str(smoothingParam["smoothingGaussianBlurSigmaX"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaX)

                annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaY = annotations.new_tag('GaussianBlurSigmaY')
                annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaY.string = str(smoothingParam["smoothingGaussianBlurSigmaY"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_GaussianBlurring_SigmaY)

                annot_smoothingParams_Param_smoothingName_GaussianBlurring_BorderType = annotations.new_tag('GaussianBlurBorderType')
                annot_smoothingParams_Param_smoothingName_GaussianBlurring_BorderType.string = str(smoothingParam["smoothingGaussianBlurBorderType"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_GaussianBlurring_BorderType)
            
            elif (str(smoothingParam["smoothingType"]) == "Bilateral Filtering"):
                annot_smoothingParams_Param_smoothingName_BilateralFiltering_FilterSize = annotations.new_tag('BilateralFilterSize')
                annot_smoothingParams_Param_smoothingName_BilateralFiltering_FilterSize.string = str(smoothingParam["smoothingBilateralFilterFilterSize"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_BilateralFiltering_FilterSize)

                annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaColor = annotations.new_tag('BilateralFilterSigmaColor')
                annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaColor.string = str(smoothingParam["smoothingBilateralFilterSigmaColor"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaColor)

                annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaSpace = annotations.new_tag('BilateralFilterSigmaSpace')
                annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaSpace.string = str(smoothingParam["smoothingBilateralFilterSigmaSpace"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_BilateralFiltering_SigmaSpace)

                annot_smoothingParams_Param_smoothingName_BilateralFiltering_BorderType = annotations.new_tag('BilateralFilterBorderType')
                annot_smoothingParams_Param_smoothingName_BilateralFiltering_BorderType.string = str(smoothingParam["smoothingBilateralFilterBorderType"])
                annot_smoothingParams_Method.append(annot_smoothingParams_Param_smoothingName_BilateralFiltering_BorderType)


    # Annotations for Detection Params
    annot_detectionParams = annotations.new_tag('DETECTION_PARAMS')
    annotations.append(annot_detectionParams)


    annot_detectionParams_Method = annotations.new_tag('Detection_Method')
    annot_detectionParams_Method.string = str(detectionParams["selectDetectionMethod"])
    annot_detectionParams.append(annot_detectionParams_Method)


    if (detectionParams["selectDetectionMethod"] == "Thresholding"):
        annot_detectionParams_Method_Thresholding_ThreshVal = annotations.new_tag('Thresholding_ThreshVal')
        annot_detectionParams_Method_Thresholding_ThreshVal.string = str(detectionParams["detectionMethodThresh_ThreshVal"])
        annot_detectionParams.append(annot_detectionParams_Method_Thresholding_ThreshVal)

        annot_detectionParams_Method_Thresholding_MaxVal = annotations.new_tag('Thresholding_MaxVal')
        annot_detectionParams_Method_Thresholding_MaxVal.string = str(detectionParams["detectionMethodThresh_MaxVal"])
        annot_detectionParams.append(annot_detectionParams_Method_Thresholding_MaxVal)

        annot_detectionParams_Method_Thresholding_Type = annotations.new_tag('Thresholding_Type')
        annot_detectionParams_Method_Thresholding_Type.string = str(detectionParams["detectionMethodThresh_Type"])
        annot_detectionParams.append(annot_detectionParams_Method_Thresholding_Type)

    elif (detectionParams["selectDetectionMethod"] == "Background Subtraction"):
        annot_detectionParams_Method_BGSubtraction = annotations.new_tag('SubTractMethod')
        annot_detectionParams_Method_BGSubtraction.string = str(detectionParams["detectionMethodBackSub_BackSubMethod"])
        annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction)

        if (detectionParams["detectionMethodBackSub_BackSubMethod"] == "KNN"):
            annot_detectionParams_Method_BGSubtraction_KNN_History = annotations.new_tag('KNN_History')
            annot_detectionParams_Method_BGSubtraction_KNN_History.string = str(detectionParams["backgroundSubtractionMethodKNNHistory"])
            annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction_KNN_History)

            annot_detectionParams_Method_BGSubtraction_KNN_Threshold = annotations.new_tag('KNN_Threshold')
            annot_detectionParams_Method_BGSubtraction_KNN_Threshold.string = str(detectionParams["backgroundSubtractionMethodKNNThreshold"])
            annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction_KNN_Threshold)

            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows = annotations.new_tag('KNN_DetectShadows')
            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows.string = str(detectionParams["backgroundSubtractionMethodKNNDetectShadows"])
            annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows)

            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsValue = annotations.new_tag('KNN_ShadowsValue')
            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsValue.string = str(detectionParams["backgroundSubtractionMethodKNNShadowsValue"])
            annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsValue)

            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsThreshold = annotations.new_tag('KNN_ShadowsThreshold')
            annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsThreshold.string = str(detectionParams["backgroundSubtractionMethodKNNShadowsThreshold"])
            annot_detectionParams.append(annot_detectionParams_Method_BGSubtraction_KNN_DetectShadows_ShadowsThreshold)

    if (detectionParams["selectDetectionMethod"] == "Thresholding") or (detectionParams["selectDetectionMethod"] == "Background Subtraction"):
        annot_detectionParams_Method_contoursDetection_Method = annotations.new_tag('ContourDetection_Method')
        annot_detectionParams_Method_contoursDetection_Method.string = str(detectionParams["contoursDetectionMethod"])
        annot_detectionParams.append(annot_detectionParams_Method_contoursDetection_Method)

        annot_detectionParams_Method_contoursDetection_Mode = annotations.new_tag('ContourDetection_Mode')
        annot_detectionParams_Method_contoursDetection_Mode.string = str(detectionParams["contoursDetectionMode"])
        annot_detectionParams.append(annot_detectionParams_Method_contoursDetection_Mode)

        annot_detectionParams_Method_contoursDetection_MinArea = annotations.new_tag('ContourDetection_MinArea')
        annot_detectionParams_Method_contoursDetection_MinArea.string = str(detectionParams["contoursDetectionMinArea"])
        annot_detectionParams.append(annot_detectionParams_Method_contoursDetection_MinArea)

        annot_detectionParams_Method_contoursDetection_MaxArea = annotations.new_tag('ContourDetection_MaxArea')
        annot_detectionParams_Method_contoursDetection_MaxArea.string = str(detectionParams["contoursDetectionMaxArea"])
        annot_detectionParams.append(annot_detectionParams_Method_contoursDetection_MaxArea)


    if (detectionParams["selectDetectionMethod"] == "Single Object Bounding Box") or (detectionParams["selectDetectionMethod"] == "Thresholding") or (detectionParams["selectDetectionMethod"] == "Background Subtraction"):
        annot_detectionParams_Method_PreLabel = annotations.new_tag('Prelabelling')
        annot_detectionParams_Method_PreLabel.string = str(detectionParams["detectionFeaturesPreLabelDetections"])
        annot_detectionParams.append(annot_detectionParams_Method_PreLabel)

        annot_detectionParams_Method_PreLabel_entry = annotations.new_tag('PreLabel_Entry')
        annot_detectionParams_Method_PreLabel_entry.string = str(detectionParams["detectionFeaturesPreLabelDetectionsEntry"])
        annot_detectionParams.append(annot_detectionParams_Method_PreLabel_entry)


        annot_detectionParams_Method_EnlargeBBoxes = annotations.new_tag('EnlargeBBoxes')
        annot_detectionParams_Method_EnlargeBBoxes.string = str(detectionParams["detectionFeaturesEnlargeBBoxes"])
        annot_detectionParams.append(annot_detectionParams_Method_EnlargeBBoxes)

        annot_detectionParams_Method_EnlargeBBoxes_entry = annotations.new_tag('EnlargeBBoxes_Entry')
        annot_detectionParams_Method_EnlargeBBoxes_entry.string = str(detectionParams["detectionFeaturesEnlargeBBoxesEntry"])
        annot_detectionParams.append(annot_detectionParams_Method_EnlargeBBoxes_entry)


    if (detectionParams["selectDetectionMethod"] == "Thresholding") or (detectionParams["selectDetectionMethod"] == "Background Subtraction"):
        annot_detectionParams_Method_IgnoreOverlappingBBoxes = annotations.new_tag('IgnoreOverlappingBBoxes')
        annot_detectionParams_Method_IgnoreOverlappingBBoxes.string = str(detectionParams["detectionFeaturesIgnoreOverlappingBBoxes"])
        annot_detectionParams.append(annot_detectionParams_Method_IgnoreOverlappingBBoxes)

        annot_detectionParams_Method_IgnoreOverlappingBBoxes_entry = annotations.new_tag('IgnoreOverlappingBBoxes_Entry')
        annot_detectionParams_Method_IgnoreOverlappingBBoxes_entry.string = str(detectionParams["detectionFeaturesIgnoreOverlappingBBoxesEntry"])
        annot_detectionParams.append(annot_detectionParams_Method_IgnoreOverlappingBBoxes_entry)

        annot_detectionParams_Method_RemoveBG = annotations.new_tag('RemoveBG')
        annot_detectionParams_Method_RemoveBG.string = str(detectionParams["detectionFeaturesRemoveBG"])
        annot_detectionParams.append(annot_detectionParams_Method_RemoveBG)


    # Annotations for tracking Params
    annot_trackingParams = annotations.new_tag('TRACKING_PARAMS')
    annotations.append(annot_trackingParams)


    annot_trackingParams_Method = annotations.new_tag('Tracking_Method')
    annot_trackingParams_Method.string = str(trackingParams["selectTrackingMethod"])
    annot_trackingParams.append(annot_trackingParams_Method)

    if (trackingParams["selectTrackingMethod"] == "Kalman Filter"):
        annot_trackingParams_Method_KF_Noise = annotations.new_tag('KFNoise')
        annot_trackingParams_Method_KF_Noise.string = str(trackingParams["trackingMethodKalmanFilterParametersNoise"])
        annot_trackingParams.append(annot_trackingParams_Method_KF_Noise)

        annot_trackingParams_Method_KF_TimeStep = annotations.new_tag('KFTimeStep')
        annot_trackingParams_Method_KF_TimeStep.string = str(trackingParams["trackingMethodKalmanFilterParametersTimeStep"])
        annot_trackingParams.append(annot_trackingParams_Method_KF_TimeStep)

        annot_trackingParams_Method_KF_MaxDistance = annotations.new_tag('KFMaxDistance')
        annot_trackingParams_Method_KF_MaxDistance.string = str(trackingParams["trackingMethodKalmanFilterParametersMaxDistance"])
        annot_trackingParams.append(annot_trackingParams_Method_KF_MaxDistance)


    # Shaping the annotation properly
    pretty_annot = annotations.prettify()
    pretty_annot = re.sub('<SMOOTHING_PARAMS>[ \n]+', '<SMOOTHING_PARAMS>\n', pretty_annot)

    pretty_annot = re.sub('<Smoothing_Method>[ \n]+', '\t<Smoothing_Method>\n', pretty_annot)
    pretty_annot = re.sub('</Smoothing_Method>', '\t</Smoothing_Method>', pretty_annot)
    

    pretty_annot = re.sub('<SmoothingName>[ \n]+', '\t\t<SmoothingName>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</SmoothingName>[ \n]+', '</SmoothingName>\n', pretty_annot)

    pretty_annot = re.sub('<AverageBlurKernel>[ \n]+', '\t\t\t<AverageBlurKernel>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</AverageBlurKernel>[ \n]+', '</AverageBlurKernel>\n', pretty_annot)
    pretty_annot = re.sub('<AverageBlurBorderType>[ \n]+', '\t\t\t<AverageBlurBorderType>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</AverageBlurBorderType>[ \n]+', '</AverageBlurBorderType>\n', pretty_annot)

    pretty_annot = re.sub('<MedianBlurKernel>[ \n]+', '\t\t\t<MedianBlurKernel>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</MedianBlurKernel>[ \n]+', '</MedianBlurKernel>\n', pretty_annot)

    pretty_annot = re.sub('<GaussianBlurKernel>[ \n]+', '\t\t\t<GaussianBlurKernel>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</GaussianBlurKernel>[ \n]+', '</GaussianBlurKernel>\n', pretty_annot)
    pretty_annot = re.sub('<GaussianBlurSigmaX>[ \n]+', '\t\t\t<GaussianBlurSigmaX>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</GaussianBlurSigmaX>[ \n]+', '</GaussianBlurSigmaX>\n', pretty_annot)
    pretty_annot = re.sub('<GaussianBlurSigmaY>[ \n]+', '\t\t\t<GaussianBlurSigmaY>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</GaussianBlurSigmaY>[ \n]+', '</GaussianBlurSigmaY>\n', pretty_annot)
    pretty_annot = re.sub('<GaussianBlurBorderType>[ \n]+', '\t\t\t<GaussianBlurBorderType>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</GaussianBlurBorderType>[ \n]+', '</GaussianBlurBorderType>\n', pretty_annot)

    pretty_annot = re.sub('<BilateralFilterSize>[ \n]+', '\t\t\t<BilateralFilterSize>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</BilateralFilterSize>[ \n]+', '</BilateralFilterSize>\n', pretty_annot)
    pretty_annot = re.sub('<BilateralFilterSigmaColor>[ \n]+', '\t\t\t<BilateralFilterSigmaColor>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</BilateralFilterSigmaColor>[ \n]+', '</BilateralFilterSigmaColor>\n', pretty_annot)
    pretty_annot = re.sub('<BilateralFilterSigmaSpace>[ \n]+', '\t\t\t<BilateralFilterSigmaSpace>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</BilateralFilterSigmaSpace>[ \n]+', '</BilateralFilterSigmaSpace>\n', pretty_annot)
    pretty_annot = re.sub('<BilateralFilterBorderType>[ \n]+', '\t\t\t<BilateralFilterBorderType>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</BilateralFilterBorderType>[ \n]+', '</BilateralFilterBorderType>\n', pretty_annot)

    
    pretty_annot = re.sub('<DETECTION_PARAMS>[ \n]+', '<DETECTION_PARAMS>\n', pretty_annot)

    pretty_annot = re.sub('<Detection_Method>[ \n]+', '\t<Detection_Method>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Detection_Method>[ \n]+', '</Detection_Method>\n', pretty_annot)

    pretty_annot = re.sub('<Thresholding_ThreshVal>[ \n]+', '\t\t<Thresholding_ThreshVal>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Thresholding_ThreshVal>[ \n]+', '</Thresholding_ThreshVal>\n', pretty_annot)
    pretty_annot = re.sub('<Thresholding_MaxVal>[ \n]+', '\t\t<Thresholding_MaxVal>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Thresholding_MaxVal>[ \n]+', '</Thresholding_MaxVal>\n', pretty_annot)
    pretty_annot = re.sub('<Thresholding_Type>[ \n]+', '\t\t<Thresholding_Type>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Thresholding_Type>[ \n]+', '</Thresholding_Type>\n', pretty_annot)
 
    pretty_annot = re.sub('<SubTractMethod>[ \n]+', '\t\t<SubTractMethod>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</SubTractMethod>[ \n]+', '</SubTractMethod>\n', pretty_annot)

    pretty_annot = re.sub('<KNN_History>[ \n]+', '\t\t\t<KNN_History>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KNN_History>[ \n]+', '</KNN_History>\n', pretty_annot)
    pretty_annot = re.sub('<KNN_Threshold>[ \n]+', '\t\t\t<KNN_Threshold>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KNN_Threshold>[ \n]+', '</KNN_Threshold>\n', pretty_annot)
    pretty_annot = re.sub('<KNN_DetectShadows>[ \n]+', '\t\t\t<KNN_DetectShadows>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KNN_DetectShadows>[ \n]+', '</KNN_DetectShadows>\n', pretty_annot)
    pretty_annot = re.sub('<KNN_ShadowsValue>[ \n]+', '\t\t\t<KNN_ShadowsValue>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KNN_ShadowsValue>[ \n]+', '</KNN_ShadowsValue>\n', pretty_annot)
    pretty_annot = re.sub('<KNN_ShadowsThreshold>[ \n]+', '\t\t\t<KNN_ShadowsThreshold>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KNN_ShadowsThreshold>[ \n]+', '</KNN_ShadowsThreshold>\n', pretty_annot)

    pretty_annot = re.sub('<ContourDetection_Method>[ \n]+', '\t\t<ContourDetection_Method>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</ContourDetection_Method>[ \n]+', '</ContourDetection_Method>\n', pretty_annot)
    pretty_annot = re.sub('<ContourDetection_Mode>[ \n]+', '\t\t<ContourDetection_Mode>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</ContourDetection_Mode>[ \n]+', '</ContourDetection_Mode>\n', pretty_annot)
    pretty_annot = re.sub('<ContourDetection_MinArea>[ \n]+', '\t\t<ContourDetection_MinArea>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</ContourDetection_MinArea>[ \n]+', '</ContourDetection_MinArea>\n', pretty_annot)
    pretty_annot = re.sub('<ContourDetection_MaxArea>[ \n]+', '\t\t<ContourDetection_MaxArea>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</ContourDetection_MaxArea>[ \n]+', '</ContourDetection_MaxArea>\n', pretty_annot)

    pretty_annot = re.sub('<Prelabelling>[ \n]+', '\t\t<Prelabelling>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Prelabelling>[ \n]+', '</Prelabelling>\n', pretty_annot)
    pretty_annot = re.sub('<PreLabel_Entry>[ \n]+', '\t\t\t<PreLabel_Entry>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</PreLabel_Entry>[ \n]+', '</PreLabel_Entry>\n', pretty_annot)

    pretty_annot = re.sub('<EnlargeBBoxes>[ \n]+', '\t\t<EnlargeBBoxes>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</EnlargeBBoxes>[ \n]+', '</EnlargeBBoxes>\n', pretty_annot)
    pretty_annot = re.sub('<EnlargeBBoxes_Entry>[ \n]+', '\t\t\t<EnlargeBBoxes_Entry>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</EnlargeBBoxes_Entry>[ \n]+', '</EnlargeBBoxes_Entry>\n', pretty_annot)

    pretty_annot = re.sub('<IgnoreOverlappingBBoxes>[ \n]+', '\t\t<IgnoreOverlappingBBoxes>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</IgnoreOverlappingBBoxes>[ \n]+', '</IgnoreOverlappingBBoxes>\n', pretty_annot)
    pretty_annot = re.sub('<IgnoreOverlappingBBoxes_Entry>[ \n]+', '\t\t\t<IgnoreOverlappingBBoxes_Entry>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</IgnoreOverlappingBBoxes_Entry>[ \n]+', '</IgnoreOverlappingBBoxes_Entry>\n', pretty_annot)

    pretty_annot = re.sub('<RemoveBG>[ \n]+', '\t\t<RemoveBG>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</RemoveBG>[ \n]+', '</RemoveBG>\n', pretty_annot)

    pretty_annot = re.sub('<TRACKING_PARAMS>[ \n]+', '<TRACKING_PARAMS>\n', pretty_annot)

    pretty_annot = re.sub('<Tracking_Method>[ \n]+', '\t<Tracking_Method>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</Tracking_Method>[ \n]+', '</Tracking_Method>\n', pretty_annot)
    pretty_annot = re.sub('<KFNoise>[ \n]+', '\t\t<KFNoise>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KFNoise>[ \n]+', '</KFNoise>\n', pretty_annot)
    pretty_annot = re.sub('<KFTimeStep>[ \n]+', '\t\t<KFTimeStep>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KFTimeStep>[ \n]+', '</KFTimeStep>\n', pretty_annot)
    pretty_annot = re.sub('<KFMaxDistance>[ \n]+', '\t\t<KFMaxDistance>', pretty_annot)
    pretty_annot = re.sub('[ \n]+</KFMaxDistance>[ \n]+', '</KFMaxDistance>\n', pretty_annot)

    return pretty_annot
