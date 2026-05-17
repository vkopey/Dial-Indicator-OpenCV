import cv2
import numpy as np

# Завантажуємо зображення
img = cv2.imread("indicator.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Виділення контурів через Canny
edges = cv2.Canny(gray, 50, 150)
cv2.imshow("indicator", edges)

# Пошук контурів
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Завантажуємо шаблон стрілки (контур)
tpl = cv2.imread("arrow_template.png", cv2.IMREAD_GRAYSCALE)

tpl_edges = cv2.Canny(tpl, 50, 150)
cv2.imshow("Arrow", tpl_edges)
tpl_contours, _ = cv2.findContours(tpl_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt_tpl = max(tpl_contours, key=cv2.contourArea)


img.fill(255)
#cv2.drawContours(img, [cnt_tpl], -1, (0,255,0), 2)
#for cnt in contours[0:3]:
#    cv2.drawContours(img, [cnt], -1, (0,255,0), 2)

# Перевіряємо кожен контур на схожість

for i,cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area < 300 or area > 5000:  # фільтр за площею
        continue

    score = cv2.matchShapes(cnt_tpl, cnt, cv2.CONTOURS_MATCH_I3, 0.0)
    if score < 0.5:  # поріг схожості
        cv2.drawContours(img, [cnt], -1, (0,255,0), 1)
        print("Знайдено стрілку!", i)

cv2.imshow("Detected Arrow", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
