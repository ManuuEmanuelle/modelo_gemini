import os
import fitz

from .pre_processing import criar_pastas, listar_pdfs, obter_paginas_exame
from .extracao import extrair_texto_exame, extrair_texto_laudo, salvar_json_exames

def processar_pdfs(pdf_folder, dados):

    (
        exames_json_folder,
        laudos_text_folder,
    ) = criar_pastas(dados)

    arquivos_pdf = listar_pdfs(pdf_folder)

    for i, file in enumerate(arquivos_pdf, start=1):

        paciente = f"paciente_{i}"

        json_resultado_path = os.path.join(exames_json_folder, paciente)

        if os.path.exists(json_resultado_path):
            print("Pdf já processado")
            continue

        pdf_path = os.path.join(pdf_folder, file)


        doc = fitz.open(pdf_path)

        num_paginas = len(doc)

        paginas_exame = obter_paginas_exame(num_paginas)

        if paginas_exame is None:

            print(f"PDF inválido: {file}")

            doc.close()

            continue

        '''extrair_imagens_exame(
            pdf_path,
            paginas_exame,
            exame_image_folder,
            paciente
        )'''

        exames = extrair_texto_exame(
            doc,
            paginas_exame
        )

        salvar_json_exames(
            exames,
            paciente,
            exames_json_folder
        )

        '''extrair_imagens_laudos(
            pdf_path,
            laudos_image_folder,
            num_paginas,
            paciente
        )'''

        extrair_texto_laudo(
            doc,
            laudos_text_folder,
            paciente
        )

        doc.close()

        print(
            f"{paciente} processado com "
            f"{len(paginas_exame)} exame(s)"
        )