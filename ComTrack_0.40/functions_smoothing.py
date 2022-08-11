### Functions that are used in videoTrack_VideaoThread.py
import cv2

def applySmoothing(frame, smoothingParam):
    if (smoothingParam["smoothingActivated"] == True):
        if smoothingParam["smoothingType"] == "Averaging":
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_DEFAULT': BorderType = cv2.BORDER_DEFAULT
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_CONSTANT': BorderType = cv2.BORDER_CONSTANT
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_REPLICATE': BorderType = cv2.BORDER_REPLICATE
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_REFLECT': BorderType = cv2.BORDER_REFLECT
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_TRANSPARENT': BorderType = cv2.BORDER_TRANSPARENT
            if smoothingParam["smoothingAverageBlurBorderType"] == 'BORDER_ISOLATED': BorderType = cv2.BORDER_ISOLATED
            newFrame = cv2.blur(src=frame, ksize=(smoothingParam["smoothingAverageBlurKernel"], smoothingParam["smoothingAverageBlurKernel"]), borderType=BorderType)
        if smoothingParam["smoothingType"] == "Median Blurring":
            newFrame = cv2.medianBlur(src=frame, ksize=smoothingParam[ "smoothingMedianBlurKernel"])
        if smoothingParam["smoothingType"] == "Gaussian Blurring":
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_DEFAULT': BorderType = cv2.BORDER_DEFAULT
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_CONSTANT': BorderType = cv2.BORDER_CONSTANT
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_REPLICATE': BorderType = cv2.BORDER_REPLICATE
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_REFLECT': BorderType = cv2.BORDER_REFLECT
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_TRANSPARENT': BorderType = cv2.BORDER_TRANSPARENT
            if smoothingParam["smoothingGaussianBlurBorderType"] == 'BORDER_ISOLATED': BorderType = cv2.BORDER_ISOLATED
            newFrame = cv2.GaussianBlur(src=frame, ksize=(smoothingParam["smoothingGaussianBlurKernel"], smoothingParam["smoothingGaussianBlurKernel"]), sigmaX=smoothingParam["smoothingGaussianBlurSigmaX"], sigmaY=smoothingParam["smoothingGaussianBlurSigmaY"], borderType=BorderType)
        if smoothingParam["smoothingType"] == "Bilateral Filtering":
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_DEFAULT': BorderType = cv2.BORDER_DEFAULT
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_CONSTANT': BorderType = cv2.BORDER_CONSTANT
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_REPLICATE': BorderType = cv2.BORDER_REPLICATE
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_REFLECT': BorderType = cv2.BORDER_REFLECT
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_TRANSPARENT': BorderType = cv2.BORDER_TRANSPARENT
            if smoothingParam["smoothingBilateralFilterBorderType"] == 'BORDER_ISOLATED': BorderType = cv2.BORDER_ISOLATED
            newFrame = cv2.bilateralFilter(src=frame, d=smoothingParam["smoothingBilateralFilterFilterSize"], sigmaColor=smoothingParam["smoothingBilateralFilterSigmaColor"], sigmaSpace=smoothingParam["smoothingBilateralFilterSigmaSpace"], borderType=BorderType)
    else:
        newFrame = frame
    return newFrame
