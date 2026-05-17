import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# 1. Виявлення ліній
img = cv2.imread("indicator.png", cv2.IMREAD_GRAYSCALE)
edges = cv2.Canny(img, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                        minLineLength=50, maxLineGap=10)

# 2. Формування ознак
def extract_features(line, center):
    x1,y1,x2,y2 = line[0]
    length = np.hypot(x2-x1, y2-y1)
    angle = np.degrees(np.arctan2(y2-y1, x2-x1))
    dist1 = np.hypot(x1-center[0], y1-center[1])
    dist2 = np.hypot(x2-center[0], y2-center[1])
    return [length, angle, min(dist1, dist2)]

model = RandomForestClassifier(n_estimators=5, max_depth=3)
x=np.array([[0,1,1,2,2,3,2,3,1,3, 6,5,6,7,7,8,7,7,8,5],
            [1,1,3,1,2,2,3,4,4,8, 5,7,6,7,6,7,5,8,8,1],
            [1,1,3,1,2,2,3,4,4,8, 5,7,6,7,6,7,5,8,8,1]])
y=np.array( [0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,1] )
x=x.T
model.fit(x, y)  # навчання на підготовлених даних

# 3. Класифікація ліній
center = (img.shape[1]//2, img.shape[0]//2)
for line in lines:
    features = extract_features(line, center)
    pred = model.predict([features])  # 0 = шум, 1 = стрілка
    if pred == 1:
        x1,y1,x2,y2 = line[0]
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)

cv2.imshow("Detected Arrow", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
