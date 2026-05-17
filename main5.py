import cv2

# Завантажуємо зображення
img = cv2.imread("indicator.png", cv2.IMREAD_GRAYSCALE)
tpl = cv2.imread("arrow_template.png", cv2.IMREAD_GRAYSCALE)

# Ініціалізація ORB
orb = cv2.ORB_create()

# Знаходимо ключові точки та дескриптори
kp1, des1 = orb.detectAndCompute(tpl, None)
kp2, des2 = orb.detectAndCompute(img, None)

# Порівняння дескрипторів
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Сортуємо за якістю
matches = sorted(matches, key=lambda x: x.distance)

# Візуалізація перших 20 збігів
result = cv2.drawMatches(tpl, kp1, img, kp2, matches[:20], None, flags=2)

cv2.imshow("Feature Matching", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
