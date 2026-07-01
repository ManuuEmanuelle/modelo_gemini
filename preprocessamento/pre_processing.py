import os
import re

def criar_pastas(base_dir):

    exame_folder = os.path.join(base_dir, "exames_texto")
    laudos_folder = os.path.join(base_dir, "laudos_texto")

    os.makedirs(exame_folder, exist_ok=True)
    os.makedirs(laudos_folder, exist_ok=True)

    return exame_folder, laudos_folder

def extrair_numero(nome_arquivo):
    numeros = re.findall(r'\d+', nome_arquivo)
    return tuple(map(int, numeros)) if numeros else (0,)

def listar_pdfs(pdf_folder):

    arquivos_pdf = [
        f for f in os.listdir(pdf_folder)
        if f.endswith(".pdf")
    ]

    arquivos_pdf.sort(key=extrair_numero)

    return arquivos_pdf

def obter_paginas_exame(num_paginas):

    if num_paginas >= 3:
        return [1, 2]

    elif num_paginas == 2:
        return [1]

    return None

'''def borrar_regiao_exame(img):

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

def extrair_imagens(pdf_path, paginas_exame, exame_folder, paciente):

    images = []

    for pagina in paginas_exame:

        imgs = convert_from_path(
            pdf_path,
            first_page=pagina,
            last_page=pagina
        )

        images.extend(imgs)

    for j, img in enumerate(images, start=1):

        img = borrar_regiao_exame(img)

        img_path = os.path.join(
            exame_folder,
            f"{paciente}_exame_{j}.png"
        )

        cv2.imwrite(img_path, img)

def extrair_texto_laudo(doc, laudos_folder, paciente):
    num_paginas = len(doc)
    text = doc[num_paginas-1].get_text()

    text_path = os.path.join(
        laudos_folder,
        f"{paciente}.txt"
    )

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

def processar_pdfs(pdf_folder, dados):

    exame_folder, laudos_folder = criar_pastas(dados)

    arquivos_pdf = listar_pdfs(pdf_folder)

    for i, file in enumerate(arquivos_pdf, start=1):

        pdf_path = os.path.join(pdf_folder, file)

        paciente = f"paciente_{i}"

        doc = fitz.open(pdf_path)

        num_paginas = len(doc)

        paginas_exame = obter_paginas_exame(num_paginas)

        if paginas_exame is None:

            print(f"PDF inválido: {file}")

            doc.close()

            continue

        images = extrair_imagens(pdf_path, paginas_exame, exame_folder, paciente)

      
        extrair_texto_laudo(doc, laudos_folder, paciente)

    
        doc.close()

        print(
            f"{paciente} processado com "
            f"{len(images)} exame(s)"
        )




def borrar_regiao_laudo(img):
    imagem = np.array(img)

def processar_pdfs(pdf_folder, dados):

    exame_folder = os.path.join(dados, "exames_imagem")
    laudos_folder = os.path.join(dados, "laudos_texto")

    os.makedirs(exame_folder, exist_ok=True)
    os.makedirs(laudos_folder, exist_ok=True)

    arquivos_pdf = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    arquivos_pdf.sort(key=extrair_numero)

    for i, file in enumerate(arquivos_pdf, start=1):

        pdf_path = os.path.join(pdf_folder, file)
        paciente = f"paciente_{i}"

        doc = fitz.open(pdf_path)
        num_paginas = len(doc)

        if num_paginas >= 3:

            paginas_exame = [1, 2]

        elif num_paginas == 2:

            paginas_exame = [1]

        else:
            print(f"PDF inválido (menos de 2 páginas): {file}")
            doc.close()
            continue

    
        images = []

        for pagina in paginas_exame:

            imgs = convert_from_path(
                pdf_path,
                first_page=pagina,
                last_page=pagina
            )

            images.extend(imgs)

        for j, img in enumerate(images, start=1):

            img = borrar_regiao_exame(img)

            img_path = os.path.join(
                exame_folder,
                f"{paciente}_exame_{j}.png"
            )

            cv2.imwrite(img_path, img)

        text = doc[num_paginas - 1].get_text()

        doc.close()

        text_path = os.path.join(
            laudos_folder,
            f"{paciente}.txt"
        )

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"{paciente} processado com {len(images)} exame(s)")'''


