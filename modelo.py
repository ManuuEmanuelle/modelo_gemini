from dotenv import load_dotenv
import os
import time
import re
import json


import google.generativeai as genai 



load_dotenv()

#client = genai.Client()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def carregar_json_exame(
    exames_json_folder,
    paciente
):

    json_path = os.path.join(
        exames_json_folder,
        f"{paciente}.json"
    )

    with open(
        json_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def gerar_laudo(dados_exame):

    model = genai.GenerativeModel(
        "models/gemini-2.5-flash"
    )

    prompt = f"""
    Você é um oftalmologista especialista em glaucoma e campimetria computadorizada.
Sua tarefa é gerar um laudo clínico utilizando exclusivamente os dados estruturados do exame fornecidos abaixo.

--------------------------------------------------
DADOS DO EXAME (JSON)
{dados_exame}

--------------------------------------------------
DIRETRIZES DE INTERPRETAÇÃO (REGRAS DE NEGÓCIO)

Você deve traduzir as classificações textuais contidas no JSON (como "leve", "alterado", "normal", "preservado", "ruim") em descrições semânticas médicas e formais.

Como converter as classificações em prosa médica (Exemplos):

[INCORRETO - Formato de Lista / Rótulo Seco]
- Fóvea: muito reduzida
- MD: grave
- PSD: alterado
- Erros de fixação: ruim

[CORRETO - Texto Clínico Fluido]
- A sensibilidade foveal encontra-se severamente deprimida.
- O desvio médio (MD) demonstra depressão acentuada da sensibilidade global.
- O desvio padrão do modelo (PSD) encontra-se significativamente aumentado, indicando a presença de defeitos localizados (escotomas).
- Os índices de confiabilidade apontam uma taxa de perda de fixação inadequada, comprometendo a fidelidade do teste.

--------------------------------------------------
RESTRIÇÕES DE ESCRITA OBRIGATÓRIAS

1. NUNCA exponha a mecânica do código no laudo. Não cite termos como "_classificacao", "JSON", "chaves", "variáveis" ou os rótulos literais isolados.
2. NUNCA infira dados ausentes: idade, sexo, histórico clínico, pressão intraocular, tempo de doença ou progressão (a menos que haja mais de um exame sequencial explicitamente detalhado no input).
3. Se um parâmetro não constar no JSON do exame (ex: CPSD ou SFh omitidos na estratégia SITA), cite textualmente que o índice "não foi avaliado nesta estratégia de exame".
4. Caso os índices de confiabilidade gerais estejam classificados como "ruim", declare explicitamente no laudo: "Exame com baixa confiabilidade técnica".

--------------------------------------------------
FORMATO OBRIGATÓRIO DE SAÍDA

LAUDO DE CAMPIMETRIA COMPUTADORIZADA

1. ACHADOS CLÍNICOS

- Olho Direito (OD) [Se presente no JSON]
  * Confiabilidade Técnica: (Interpretar erros de fixação, falsos positivos e falsos negativos)
  * Sensibilidade Foveal: (Descrever o estado da fóvea)
  * Índices Globais: (Descrever MS, MD/MDh, VFI/VQi de forma textual e fluida, citando o valor numérico bruto ao lado entre parênteses)
  * Análise de Hemicampus (GHT): (Descrever o resultado semântico do GHT)
  * Padrão de Perda Regional: (Descrever o PSD/CPSD e se há defeitos locais)

- Olho Esquerdo (OE) [Se presente no JSON]
  * Confiabilidade Técnica: (Interpretar erros de fixação, falsos positivos e falsos negativos)
  * Sensibilidade Foveal: (Descrever o estado da fóvea)
  * Índices Globais: (Descrever MS, MD/MDh, VFI/VQi de forma textual e fluida, citando o valor numérico bruto ao lado entre parênteses)
  * Análise de Hemicampus (GHT): (Descrever o resultado semântico do GHT)
  * Padrão de Perda Regional: (Descrever o PSD/CPSD e se há defeitos locais)

- Correlação Interocular
  * (Comparar a simetria ou assimetria de perda entre o OD e o OE com base nos índices estruturados).

2. IMPRESSÃO DIAGNÓSTICA
- (Descrever a compatibilidade do padrão de perda encontrado com o dano glaucomatoso (ex: defeitos localizados assimétricos) e a severidade geral indicada pelo MD/VFI. Se a confiabilidade for baixa, reiterar a necessidade de repetição do exame).

3. OBSERVAÇÕES
- (Recomendações técnicas padrão: necessidade de correlação com a propedêutica de glaucoma, avaliação do disco óptico e curva tensional).

--------------------------------------------------
REGRAS DE COMPORTAMENTO DO MODELO
- Use estritamente a terceira pessoa e linguagem médica formal/técnica.
- Seja conciso: elimine termos redundantes.
- Emita APENAS o laudo final formatado, sem introduções ("Aqui está o seu laudo:") ou finalizações."""
    
    response = model.generate_content(
            [prompt]
        )

    return response.text


def extrair_numero_paciente(nome):

    numeros = re.findall(r"\d+", nome)

    return int(numeros[0]) if numeros else 0


def processar_exames(
    exames_json_folder,
    output_folder
):
    os.makedirs(
        output_folder,
        exist_ok=True
    )

    arquivos_json = [

        f for f in os.listdir(
            exames_json_folder
        )

        if f.endswith(".json")
    ]

    arquivos_json.sort(
        key=extrair_numero_paciente
    )

    tempos_path = os.path.join(output_folder, "tempos_laudos.json")

    if os.path.exists(tempos_path):
        with open(tempos_path, "r", encoding="utf-8") as f:
            tempos_path = json.load(f)

    else:
        tempos = {}


    for i, file in enumerate(
        arquivos_json
    ):

        #if i >= 25:
        #   break

        paciente = file.replace(
            ".json",
            ""
        )

        paciente_folder = os.path.join(
            output_folder,
            paciente
        )

        os.makedirs(
            paciente_folder,
            exist_ok=True
        )
        laudo_path = os.path.join(
            paciente_folder,
            "laudo.txt"
        )

        if os.path.exists(laudo_path):
            print("Laudo já existe. Pulando para o próximo")
            continue

        dados_exame = (
            carregar_json_exame(
                exames_json_folder,
                paciente
            )
        )
        
        inicio = time.time()

        laudo = gerar_laudo(
            dados_exame
        )

        fim = time.time()

        tempo_laudo = fim - inicio

        tempos[paciente] = tempo_laudo


        with open(tempos_path, "w", encoding="utf-8") as f:
            json.dump(tempos, f, indent=4,ensure_ascii=False)


        with open(
            laudo_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(laudo)

        

    if tempos_path:

        lista_tempos = list(tempos_path.values())


        media_tempo = (
            sum(lista_tempos) / len(lista_tempos)
        )

        tempo_total_execucao = sum(lista_tempos)



        print("\n--- MÉTRICAS DE EXECUÇÃO ACUMULADAS ---")
        
        print(f"Média de tempo por laudo: {media_tempo:.2f} segundos")
        print(f"Tempo total de processamento: {tempo_total_execucao:.2f} segundos")