import cv2
from tkinter import filedialog
from reportlab.pdfgen import canvas


def gerar_pdf(respostas):

    c = canvas.Canvas("relatorio.pdf")
    x=100
    y= (len(respostas)*130)-60
    espacamento=20

    # Definir o tamanho da página
    c.setPageSize((400, len(respostas)*130))

    c.setFont("Helvetica", 20)
    c.drawString(x, y+10, "Rendimento dos alunos")

    c.setFont("Helvetica", 12)


    for i,d in enumerate(respostas):
        c.drawString(x, y-espacamento, f"O aluno {i+1} teve os seguintes resultados:")
        c.drawString(x, y-espacamento*2, f'Respostas: {d[0]}')
        c.drawString(x, y-espacamento*3, f'Acertos: {d[1]}')
        c.drawString(x, y-espacamento*4, f'Pontuação: {d[2]}')

        y-=espacamento*5
    # Salvar o PDF
    c.showPage()
    c.save()

def upar_imagem():
    filename = filedialog.askopenfilename()
    return filename

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

def selecionar(img):
        img = cv2.resize(img, (600, 700))
        x, y, w, h = cv2.selectROI(img)
        recorte = img[y:y+h, x:x+w]
        recorte = cv2.resize(recorte, (400, 500))
        return recorte