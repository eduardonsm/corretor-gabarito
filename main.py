import cv2
from funcoes import gerar_pdf, upar_imagem, extrairMaiorCtn, selecionar
from tkinter import Tk, Button, messagebox, Label

campos = [(12, 2, 92, 85), (105, 2, 92, 85), (196, 2, 92, 85), (289, 2, 92, 85),
          (12, 95, 92, 85), (105, 95, 92, 85), (196, 95, 92, 85), (289, 95, 92, 85),
          (12, 187, 92, 85), (105, 187, 92, 85), (196,187, 92, 85), (289, 187, 92, 85),
          (12, 285, 92, 85), (105, 285, 92, 85), (196, 285, 92, 85), (289, 285, 92, 85),
          (12, 382, 92, 85), (105, 382, 92, 85), (196, 382, 92, 85), (289, 382, 92, 85)]
# coordenadas que correspondem a cada alternativa

resp = ['1-A', '1-B', '1-C', '1-D',
        '2-A', '2-B', '2-C', '2-D',
        '3-A', '3-B', '3-C', '3-D',
        '4-A', '4-B', '4-C', '4-D',
        '5-A', '5-B', '5-C', '5-D']
# todas as alternativas em ordem

respostasCorretas = ["1-A", "2-C", "3-B", "4-D", "5-A"]

respostas_armazenadas = []
# lista usada para armazenar os resultados das analises


def analisar_gabarito(imgTh, respostas=[]):
    for id, vg in enumerate(campos):
        x = int(vg[0])
        # coordenada x
        y = int(vg[1])
        # coordenada y
        w = int(vg[2])
        # largura width
        h = int(vg[3])
        # altura height

        # ou seja, vai atribuindo x,y,w,h para cada alternativa 

        campo = imgTh[y:y + h, x:x + w]
        # recorta a alternativa na imagem
        area = w * h
        pixel_branco = cv2.countNonZero(campo)
        # analisa quantos pixels brancos existem no campo

        percentual = float((pixel_branco / area) * 100)
        if percentual >= 10:
            respostas.append(resp[id])
        # se for mais de 10% em relacao a area do campo é adicionado nas respostas marcada pelo usuario

    acertos = 0
    if len(respostas) == len(respostasCorretas):
        for num, res in enumerate(respostas):
            if res == respostasCorretas[num]:
                print(f'{res} OK, correto: {respostasCorretas[num]}')
                acertos += 1
            else:
                print(f'{res} ERRADO, correto: {respostasCorretas[num]}')

        pontuacao = int(acertos * 2)
        # considerando que sao 5 questoes, cada questao vale 2 para resultar no maximo em 10

        cv2.waitKey(0)
        # essa funcao serve para esperar alguma tecla ser digitada
        print(f'''
        respostas corretas = {respostasCorretas}
        respostas = {respostas}
        acertos = {acertos}
        pontuacao = {pontuacao}
        ''')

        dados = [respostas, acertos, pontuacao]
        respostas_armazenadas.append(dados)
        cv2.destroyAllWindows()
        # fecha as janelas criadas, por exemplo na opcao de selecionar manualmente
    else:
        messagebox.showerror(
            "Erro", "Imagem não reconhecida! Tente selecionar manualmente ou fazer o upload de uma nova imagem.")
        # mensagem de erro caso as respostas lidas nao forem da mesma quantidade das respostas corretas

def upload_e_processar():
    filename = upar_imagem()
    if filename:
        processar_imagem(filename)
    # upa imagem e chama a funcao para processar a imagem


def processar_imagem(imagem):
    imagem_bruto = cv2.imread(imagem)
    imagem = cv2.resize(imagem_bruto, (600, 700))
    # le a imagem e redimensiona

    gabarito = extrairMaiorCtn(imagem)
    # é recortado o gabarito

    imgGray = cv2.cvtColor(gabarito, cv2.COLOR_BGR2GRAY)
    # a imagem é transformada em escala de cinza

    ret, imgTh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)
    # transforma em uma imagem binaria invertida

    respostas = []
    analisar_gabarito(imgTh, respostas)
    # cria um lista para as respostas e chama a funcao para analisar o gabarito passando a imagem binaria


def selecionar_manualmente():
    imagem = upar_imagem()
    imagem_bruto = cv2.imread(imagem)
    # upa a imagem e le

    gabarito = selecionar(imagem_bruto)
    # é extraido o gabarito pela funcao selecionar

    imgGray = cv2.cvtColor(gabarito, cv2.COLOR_BGR2GRAY)
     # a imagem é transformada em escala de cinza

    ret, imgTh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)
    # transforma em uma imagem binaria invertida

    respostas = []
    analisar_gabarito(imgTh, respostas)
    # cria um lista para as respostas e chama a funcao para analisar o gabarito passando a imagem binaria


root = Tk()
# cria uma janela

root.title("Correção por imagem")
root.configure(background='#5865f2', padx=40, pady=40)
# adiciona o titulo e algumas configuracoes de estilo

largura_janela = 400
altura_janela = 370
# define a largura e altura da janela

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
# define a largura e altura da tela do usuario

posicao_x = (largura_tela - largura_janela) // 2
posicao_y = (altura_tela - altura_janela) // 2
# calcula onde é o centro

root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
# essa funcao é usada para definir o tamanho e a posicao da janela, nesse caso esta posicionada no centro

titulo = Label(root, text="Corretor de gabarito", font=('Helvica', 20, 'bold'), fg='white', background='#5865f2')
titulo.place(relx=0.5, rely=0.12, anchor="center")
# cria um texto e posiciona centralizado horizontalmente e acima do centro vertical

button = Button(root, text="Fazer upload da Imagem", command=upload_e_processar,pady=12, padx=12, bd=0.5, font=('Arial', 12), activebackground='#d1d5ff')
button.place(relx=0.5, rely=0.45, anchor="center")
# cria um botao para fazer upload da imagem, chamando a funcao upload_e_processar 


button_selecionar_manualmente = Button(root, text="Selecionar Manualmente", command=selecionar_manualmente,padx=12, pady=12, bd=0.5, font=('Arial', 12), activebackground='#d1d5ff')
button_selecionar_manualmente.place(relx=0.5, rely=0.8, anchor="center")
# cria um botao para fazer a selecao manual da imagem, chamando a funcao selecionar_manualmente


root.mainloop()
# isso faz a janela ficar em loop ate ser fechado

gerar_pdf(respostas_armazenadas)
print("PDF do rendimento gerado com sucesso.")
# gera um pdf com as respostas_armazenadas e printa uma mensagem na tela
