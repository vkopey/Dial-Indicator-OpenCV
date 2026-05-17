import cv2

# Завантажуємо зображення та шаблон
img = cv2.imread("indicator.png", cv2.IMREAD_GRAYSCALE)
template = cv2.imread("arrow_template.png", cv2.IMREAD_GRAYSCALE)


# Виділяємо контури
_, thresh_img = cv2.threshold(img, 200, 200, cv2.THRESH_OTSU)
_, thresh_tpl = cv2.threshold(template, 240, 255, cv2.THRESH_BINARY)

thresh_img = cv2.Canny(thresh_img, 50, 150)
thresh_tpl = cv2.Canny(thresh_tpl, 50, 150)

cv2.imshow("", thresh_img)
#cv2.imshow("", thresh_tpl)


contours_img, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_tpl, _ = cv2.findContours(thresh_tpl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img.fill(255)

for cont in contours_img:
    cv2.drawContours(img, [cont], -1, (0,255,0), 1)



# Беремо найбільший контур шаблону
cnt_tpl = max(contours_tpl, key=cv2.contourArea)

# Порівнюємо з контурами на зображенні
for cnt in contours_img:
    score = cv2.matchShapes(cnt_tpl, cnt, cv2.CONTOURS_MATCH_I1, 0.0)
    if score < 0.5:  # поріг схожості
        #cv2.drawContours(img, [cnt], -1, (0,255,0), 1)
        print("Знайдено стрілку з кругом у центрі!")

cv2.imshow("Detected Arrow", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
