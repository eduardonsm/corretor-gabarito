import cv2
from tkinter import filedialog
from reportlab.pdfgen import canvas


def gerar_pdf(respostas):

    c = canvas.Canvas("relatorio.pdf")
    x=100
    # coordenada x
    y= (len(respostas)*130)-60
    # coordenada y, quantidade de analises * 130 que vai ser a altura da pagina e -60 para ser um espaçamento
    espacamento=20
    # espacamento entre as frases

    c.setPageSize((400, len(respostas)*130))
    # Definir o tamanho da página (largura e altura)

    c.setFont("Helvetica", 20)
    c.drawString(x, y+10, "Rendimento dos alunos")
    # titulo do pdf com a fonte Helvetica tamanho 20

    c.setFont("Helvetica", 12)
    # setando o fonte para tamanho 12 pro resto do arquivo

    for i,d in enumerate(respostas):
    # i de indice para enumerar aluno 1, aluno 2 ...
    # d corresponde a cada dado, que é um lista com as respostas marcadas, o numero de acertos e a sua pontuação
       
        c.drawString(x, y-espacamento, f"O aluno {i+1} teve os seguintes resultados:")
        c.drawString(x, y-espacamento*2, f'Respostas: {d[0]}')
        c.drawString(x, y-espacamento*3, f'Acertos: {d[1]}')
        c.drawString(x, y-espacamento*4, f'Pontuação: {d[2]}')
    # coordenada x fixa e a coordenada y - o espacamento para ir descendo na pagina

        y -= espacamento*5
    # atualizando o valor de y para o proximo dado

    c.showPage()
    c.save()
    # fecha a pagina e salva o PDF

def upar_imagem():
    formatos = (("Imagens", "*.png;*.jpg;*.jpeg"),)
    # aqui é definido os formatos de arquivos que podem ser upados, no caso as extensoes de imagens
    arquivo = filedialog.askopenfilename(filetypes=formatos)
    return arquivo
    # é aberto o explorer para o usuario selecionar o arquivo e a funcao o retorna 

def extrairMaiorCtn(img):
    # funcao responsavel por fazer um recorte do maior contorno da imagem, no caso o gabarito

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # a imagem é transformada em escala de cinza

    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    # transforma em uma imagem binaria invertida

    contours,hi = cv2.findContours(imgTh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # procura contornos na imagem

    maiorCtn = max(contours, key = cv2.contourArea)
    # acha o maior contorno com base na area dele

    x,y,w,h = cv2.boundingRect(maiorCtn)
    # cria um retangulo no contorno e retorna as coordenadas dele

    recorte = img[y:y+h,x:x+w]
    recorte = cv2.resize(recorte,(400,500)) 
    # recorta a imagem original pra ficar so o retangulo (gabarito) e redimensiona no tamanho correto

    return recorte

def selecionar(img):
    img = cv2.resize(img, (600, 700))
    # redimensiona a imagem para facilitar a selecao

    x, y, w, h = cv2.selectROI(img)
    # essa funcao abre a imagem para o usuário desenhar um retangulo na regiao de interesse (ROI)
    # e retorna as coordenadas e as dimensoes do retangulo feito pelo usuario

    recorte = img[y:y+h, x:x+w]
    recorte = cv2.resize(recorte, (400, 500))
    # recorta a imagem original pra ficar so o retangulo (gabarito) e redimensiona no tamanho correto

    return recorte
