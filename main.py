import cv2
from funcoes import gerar_pdf, upar_imagem,extrairMaiorCtn,selecionar
from tkinter import Tk, Button, filedialog, messagebox,Label

campos = [(12, 2, 92, 85), (105, 2, 92, 85), (196, 2, 92, 85), (289, 2, 92, 85),
          (12, 95, 92, 85), (105, 95, 92, 85), (196, 95, 92, 85), (289, 95, 92, 85),
          (12, 187, 92, 85), (105, 187, 92, 85), (196, 187, 92, 85), (289, 187, 92, 85),
          (12, 285, 92, 85), (105, 285, 92, 85), (196,285, 92, 85), (289, 285, 92, 85),
          (12, 382, 92, 85), (105, 382, 92, 85), (196, 382, 92, 85), (289, 382, 92, 85)]

resp = ['1-A', '1-B', '1-C', '1-D',
        '2-A', '2-B', '2-C', '2-D',
        '3-A', '3-B', '3-C', '3-D',
        '4-A', '4-B', '4-C', '4-D',
        '5-A', '5-B', '5-C', '5-D']

respostasCorretas = ["1-A", "2-C", "3-B", "4-D", "5-A"]

respostas_armazenadas = []

def analisar_gabarito(imgTh, respostas=[]):
    for id, vg in enumerate(campos):
        x = int(vg[0])
        y = int(vg[1])
        w = int(vg[2])
        h = int(vg[3])

        campo = imgTh[y:y + h, x:x + w]
        area = w * h
        pixel_branco = cv2.countNonZero(campo)
        percentual = round((pixel_branco / area) * 100, 2)
        if percentual >= 10:
            respostas.append(resp[id])

    erros = 0
    acertos = 0
    if len(respostas) == len(respostasCorretas):
        for num, res in enumerate(respostas):
            if res == respostasCorretas[num]:
                print(f'{res} OK, correto: {respostasCorretas[num]}')
                acertos += 1
            else:
                print(f'{res} ERRADO, correto: {respostasCorretas[num]}')
                erros += 1

        pontuacao = int(acertos * 2)

        cv2.waitKey(0)

        print(f'''
        respostas corretas = {respostasCorretas}
        respostas = {respostas}
        acertos = {acertos}
        pontuacao = {pontuacao}
        ''')

        dados = [respostas,acertos,pontuacao]
        respostas_armazenadas.append(dados)
        cv2.destroyAllWindows()
    else:
        messagebox.showerror(
            "Erro", "Número de respostas obtidas não corresponde ao número de respostas corretas.")

def upload_e_processar():
    filename = upar_imagem()
    if filename:
        processar_imagem(filename)


def processar_imagem(imagem):
    imagem_bruto = cv2.imread(imagem)
    imagem = cv2.resize(imagem_bruto, (600, 700))

    gabarito = extrairMaiorCtn(imagem)
    imgGray = cv2.cvtColor(gabarito, cv2.COLOR_BGR2GRAY)
    ret, imgTh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)

    respostas = []
    analisar_gabarito(imgTh, respostas)

def selecionar_manualmente():
    imagem = upar_imagem()
    imagem_bruto = cv2.imread(imagem)

    gabarito = selecionar(imagem_bruto)

    imgGray = cv2.cvtColor(gabarito, cv2.COLOR_BGR2GRAY)
    ret, imgTh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)

    respostas = []
    analisar_gabarito(imgTh, respostas)

root = Tk()
root.title("Correção por imagem")
root.configure(background='#5865f2', padx=40, pady=40)

largura_janela = 400
altura_janela = 370

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

posicao_x = (largura_tela - largura_janela) // 2
posicao_y = (altura_tela - altura_janela) // 2

root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

titulo = Label(root, text="Corretor de gabarito", font=('Helvica', 20, 'bold'), fg='white', background='#5865f2')
titulo.place(relx=0.5, rely=0.12, anchor="center")


button = Button(root, text="Fazer upload da Imagem", command=upload_e_processar,
 pady=12, padx=12, bd=0.5, font=('Arial', 12), activebackground='#d1d5ff')

button.place(relx=0.5, rely=0.45, anchor="center")

button_selecionar_manualmente = Button(root, text="Selecionar Manualmente", command=selecionar_manualmente,
 padx=12, pady=12, bd=0.5, font=('Arial', 12), activebackground='#d1d5ff')

button_selecionar_manualmente.place(relx=0.5, rely=0.8, anchor="center")


root.mainloop()

gerar_pdf(respostas_armazenadas)
print("PDF do rendimento gerado com sucesso.")
