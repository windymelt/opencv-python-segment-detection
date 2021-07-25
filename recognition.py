import cv2
import numpy as np

idMax = 4

def getMarkerMean(ids, corners, index):
    for i, id in enumerate(ids):
        if(id[0] == index):
            v = np.mean(corners[i][0],axis=0)
            return [v[0],v[1]]
    return None

def getBasisMarker(ids, corners):
    # 左上、右上、左下、右下の順にマーカーの「中心座標」を取得
    basis = []
    basis.append(getMarkerMean(ids, corners, 0))
    basis.append(getMarkerMean(ids, corners, 1))
    basis.append(getMarkerMean(ids, corners, 2))
    basis.append(getMarkerMean(ids, corners, 3))
    return basis

def cropImage(frame, ax, ay, dx, dy):
    h = len(frame)
    w = len(frame[0])
    x1 = int(0 + w * ax)
    y1 = int(0 + h * ay)
    x2 = int(w - w * dx)
    y2 = int(h - h * dy)
    return frame[y1:y2, x1:x2]

def drawTargetArea(frame, ax, ay, dx, dy):
    h = len(frame)
    w = len(frame[0])
    x1 = 0 + w * ax
    y1 = 0 + h * ay
    x2 = w - w * dx
    y2 = h - h * dy
    cv2.drawMarker(frame, (int(x1), int(y1)), (255,0,0))
    cv2.drawMarker(frame, (int(x2), int(y1)), (255,0,0))
    cv2.drawMarker(frame, (int(x1), int(y2)), (255,0,0))
    cv2.drawMarker(frame, (int(x2), int(y2)), (255,0,0))
    return frame

def getTransformImage(target, frame,  width, height):
    frame_coordinates = np.float32(target)
    target_coordinates   = np.float32([[0, 0],[width, 0],[0, height],[width, height]])
    trans_mat = cv2.getPerspectiveTransform(frame_coordinates,target_coordinates)
    return cv2.warpPerspective(frame, trans_mat, (width, height))

def postprocess(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame,(31, 31), 0)
    threshold = 50
    th_mode = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    img_thresh = cv2.adaptiveThreshold(frame, 255, th_mode, cv2.THRESH_BINARY, 301, 10)
    return img_thresh

def main():
    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    ColorCyan = (255, 255, 0)
    frame = cv2.imread("IMG_03042.jpg") 
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    detectCount = len(ids)
    if(detectCount != idMax):
        print("detect:{} while {} required".format(detectCount, idMax))
        exit(1)
    #aruco.drawDetectedMarkers(frame, corners, ids, ColorCyan)
    basis = getBasisMarker(ids, corners)
    targetFrame = getTransformImage(basis, frame, 1500, 900)
    #targetFrame = drawTargetArea(targetFrame, 0.1, 0.13, 0.3, 0.5)
    targetFrame = cropImage(targetFrame, 0.1, 0.13, 0.3, 0.5)
    targetFrame = postprocess(targetFrame)
    cv2.imwrite("IMG_det.jpg", targetFrame)
    cv2.destroyAllWindows()

main()