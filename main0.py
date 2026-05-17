import cv2
import numpy as np
import math

# Завантажуємо зображення
img = cv2.imread("indicator.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Попередня обробка
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Пошук ліній методом Хафа
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180,
                        threshold=80, minLineLength=50, maxLineGap=10)

arrow_line = None
max_len = 0

# Вибираємо найдовшу лінію (ймовірно стрілка)
if lines is not None:
    for x1, y1, x2, y2 in lines[:,0]:
        length = math.hypot(x2 - x1, y2 - y1)
        if length > max_len:
            max_len = length
            arrow_line = (x1, y1, x2, y2)

# Обчислюємо кут стрілки
if arrow_line is not None:
    x1, y1, x2, y2 = arrow_line
    dx, dy = x2 - x1, y2 - y1
    angle = math.degrees(math.atan2(-dy, dx))  # мінус dy для корекції осі Y
    angle = (angle + 360) % 360  # нормалізація до [0,360)

    # Візуалізація
    cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 2)
    cv2.putText(img, f"Angle: {angle:.1f} deg", (50,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    print(f"Положення стрілки: {angle:.1f}°")
else:
    print("Стрілку не знайдено.")

cv2.imshow("Dial Indicator", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
