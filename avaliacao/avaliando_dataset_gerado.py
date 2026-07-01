import os
import sys

sys.path.append(os.path.dirname(__file__))

from avaliacao.metricas import calcular_bleu, calcular_rouge, similaridade_semantica

def avaliar_dataset(dataset_path, laudos_path, limite=None):

    resultados = []

    pacientes = sorted(os.listdir(dataset_path))

    for i, paciente in enumerate(pacientes):

        if limite is not None and i >= limite:
            break

        pasta_paciente = os.path.join(dataset_path, paciente)

        if not os.path.isdir(pasta_paciente):
            continue

        laudo_gerado_path = os.path.join(pasta_paciente, "laudo.txt")
        print(laudo_gerado_path)

    
        laudo_original_path = os.path.join(laudos_path, f"{paciente}_laudo.txt")
        print(laudo_original_path)

        if not os.path.exists(laudo_gerado_path):
            print(f"Sem laudo gerado: {paciente}")
            continue

        if not os.path.exists(laudo_original_path):
            print(f"Sem laudo original: {paciente}")
            continue

        with open(laudo_gerado_path, "r", encoding="utf-8") as f:
            laudo_gerado = f.read()

        with open(laudo_original_path, "r", encoding="utf-8") as f:
            laudo_original = f.read()

      
        bleu = calcular_bleu(laudo_original, laudo_gerado)
        rouge = calcular_rouge(laudo_original, laudo_gerado)
        sim = similaridade_semantica(laudo_original, laudo_gerado)

        resultados.append({
            "paciente": paciente,
            "bleu": bleu,
            "rouge": rouge,
            "sim": sim
        })

    return resultados