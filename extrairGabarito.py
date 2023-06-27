import cv2

def extrairMaiorCtn(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    # transforma em uma imagem binaria

    contours,hi = cv2.findContours(imgTh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # procura contorno na imagem (gabarito)

    maiorCtn = max(contours, key = cv2.contourArea)
    # acha o contorno com maior area

    x,y,w,h = cv2.boundingRect(maiorCtn)
    # cria um retangulo no contorno e retorna as coordenadas dele

    recorte = img[y:y+h,x:x+w]
    recorte = cv2.resize(recorte,(400,500)) 
    # recorta a imagem original pra ficar so o gabarito e redimensiona no tamanho correto

    return recorte