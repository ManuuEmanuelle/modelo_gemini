import numpy as np 
import cv2

def borrar_regiao_exame(img):

    imagem = np.array(img)

    x, y, w, h = 80, 80, 1200, 160

    regiao = imagem[y:y+h, x:x+w]

    regiao_borrada = cv2.GaussianBlur(regiao, (81, 81), 0)

    imagem[y:y+h, x:x+w] = regiao_borrada

    return imagem

def recortar_regiao_laudo(imagem):

    altura, largura = imagem.shape[:2]

    topo = int(altura * 0.15)
    rodape = int(altura * 0.85)

    imagem_recortada = imagem[topo:rodape, 0:largura]

    return imagem_recortada