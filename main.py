import numpy as np
import os

#from preprocessamento.processing import processar_pdfs
from preprocessamento.processing import processar_pdfs
from modelo import processar_exames
from avaliacao.avaliando_dataset_gerado import avaliar_dataset


def main():

    base_dir = "/home/emanuelle/Projeto de pesquisa/modelo_gemini/dados"

    pasta_pdfs = os.path.join(base_dir, "pdfs")
    #exames_imagens = os.path.join(base_dir, "exames_imagem")
    exames_texto = os.path.join(base_dir, "exames_texto")
    laudos_originais = os.path.join(base_dir, "laudos_texto")
    dataset_gerado = os.path.join(base_dir, "dataset")

    
    processar_pdfs(pasta_pdfs, base_dir)

    
    processar_exames(exames_texto, dataset_gerado)

   
    resultados = avaliar_dataset(
        dataset_gerado,
        laudos_originais,
        limite=10
    )

    
    for r in resultados:
        print(r)

  
    bleus = [r["bleu"] for r in resultados]
    rouge1 = [r["rouge"]["rouge1"].fmeasure for r in resultados]
    rougel = [r["rouge"]["rougeL"].fmeasure for r in resultados]
    sims = [r["sim"] for r in resultados]

    print("\nMÉDIAS DAS MÉTRICAS:")
    
    print(f"BLEU médio: {np.mean(bleus):.4f}")
    print(f"ROUGE-1 médio: {np.mean(rouge1):.4f}")
    print(f"ROUGE-L médio: {np.mean(rougel):.4f}")
    print(f"Similaridade semântica média: {np.mean(sims):.4f}")


if __name__ == "__main__":
    main()