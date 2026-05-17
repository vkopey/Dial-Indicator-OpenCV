import cv2
import numpy as np

def calcAngle(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    angle = np.degrees(np.arctan2(-dy, dx))  # мінус dy для корекції осі Y
    angle = (angle + 360) % 360  # нормалізація до [0,360)
    return angle

def drawLine(line, color=(0,0,255)):
    x1, y1, x2, y2, _, _, _, _  = line
    cv2.line(img, (x1, y1), (x2, y2), color, 2)

cap = cv2.VideoCapture(0)
img = cv2.imread("indicator.png")

def detect():
    "Повертає кут нахилу стрілки індикатора за допомогою OpenCV або None"
    ret, img = cap.read() # !!!!! розкоментуйте для отримання кадру з вебкамери
    (h, w) = img.shape[:2] # розміри
    center = (w // 2, h // 2)

    # тільки для тестування алгоритму
    #img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #img=cv2.rotate(img, cv2.ROTATE_180)
    # M = cv2.getRotationMatrix2D(center, 30, 1.0) # degree rotation at 1.0 scale
    # img = cv2.warpAffine(img, M, (w, h)) # Apply rotation

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Попередня обробка
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    blur=gray
    edges = cv2.Canny(blur, 50, 150)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=60, maxLineGap=5) # пошук ліній методом Хафа

    if lines[:,0].size<2:
        return

    lines1=[] # список ознак ліній
    dist1Max=0.3*center[0] #  максимальна відстань т1 до центра
    dist2Min=0.6*center[0] #  мінімальнавідстань т2 до центра
    for x1, y1, x2, y2 in lines[:,0]:
        length = np.hypot(x2 - x1, y2 - y1)
        angle=calcAngle(x1, y1, x2, y2)
        dist1 = np.hypot(x1-center[0], y1-center[1])
        dist2 = np.hypot(x2-center[0], y2-center[1])
        # тільки лінії, у яких точки розташовані близько до центру і краю
        if (dist1<dist1Max and dist2>dist2Min) or (dist2<dist1Max and dist1>dist2Min):
            lines1.append([x1, y1, x2, y2, length, angle, dist1, dist2])

    if len(lines1)<2: return
    lines1.sort(key=lambda x: x[4]) # сортування за довжиною
    arrow_line1=lines1[-1] # найдовша
    arrow_line2=lines1[-2] # друга найдовша

    # шукаємо другу лінію гострої стрілки
    i=-2
    while -i<len(lines1):
        da=abs(lines1[i][5]-arrow_line1[5])
        if 3<da<5: # тільки та друга лінія, яка відхилена на невеликий кут
            print("da=",da)
            arrow_line2=lines1[i]
            break
        else:
            print(i)
            i-=1

    for line in lines1:
        drawLine(line)
        print(line)

    drawLine(arrow_line1, (255,0,0))
    drawLine(arrow_line2, (0,255,0))

    angle=(arrow_line1[5]+arrow_line2[5])/2 # кут між лініями
    cv2.putText(img, f"{angle:.2f} deg", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Dial Indicator", img)
    return angle

if __name__=="__main__":
    print(detect())
    # while True:
    #     a=detect()
    #     print(a)
    #     if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()