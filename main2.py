import cv2
import numpy as np
import math

img = cv2.imread("indicator.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(blur, 50, 150)

# Пошук контурів
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # Апроксимація полігоном
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    if len(approx) == 3:  # трикутник
        pts = approx.reshape(-1,2)

        # Вектори сторін
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]

        # Кут між сторонами
        dot = np.dot(v1, v2)
        angle = math.degrees(math.acos(dot / (np.linalg.norm(v1)*np.linalg.norm(v2))))

        print(f"Кут між сторонами: {angle:.2f}°")

        # Визначення вістря (найменший кут)
        # Для простоти беремо вершину з найменшою сумою довжин сторін
        lengths = [np.linalg.norm(pts[(i+1)%3]-pts[i]) for i in range(3)]
        tip = pts[np.argmin(lengths)]

        # Малюємо стрілку
        cv2.drawContours(img, [approx], -1, (0,255,0), 2)
        cv2.circle(img, tuple(tip), 5, (0,0,255), -1)
        cv2.putText(img, f"{angle:.1f} deg", tuple(tip),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

cv2.imshow("Arrow Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
