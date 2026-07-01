import os
import json
import re


CAMPOS_HUMPHREY = {
    "olho": {
        "regex": r"Eye:\s*(\w+)", 
        "tipo": "str"},
    "estrategia": {
        "regex": r"Strategy:\s*([^\n\r]+)", 
        "tipo": "str"},
    "fovea": {
        "regex": r"Fovea\s*:\s*([-\d.,]+)", 
        "tipo": "float"},
    "erros_fixacao": {
        "regex": r"Fixation\s+Losses:\s*(\d+/\d+)", 
        "tipo": "str"},
    "false_pos": {
        "regex": r"False\s+POS\s+Errors:\s*([\d.,]+%)", 
        "tipo": "str"},
    "false_neg": {
        "regex": r"False\s+NEG\s+Errors:\s*([\d.,]+%)", 
        "tipo": "str"},
    "vfi": {
        "regex": r"VFI:\s*([\d.]+)", 
        "tipo": "float"},
    "md": {
        "regex": r"MD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "psd": {
        "regex": r"PSD:\s*([-\d.]+)", 
        "tipo": "float"},
    "ght": {
        "regex": r"GHT:\s*([^\n\r]+)", 
        "tipo": "str"}
}

CAMPOS_OPTOPOL = {
    "olho": {
        "regex": r"Olho:\s*(.*)", 
        "tipo": "str"},
    "erros_fixacao": {
        "regex": r"Erros\s+Fix\.\s*camera:\s*(\d+)", 
        "tipo": "int"},
    "false_pos": {
        "regex": r"FPOS:\s*(\d+/\d+)", 
        "tipo": "str"},
    "false_neg": {
        "regex": r"FNEG:\s*(\d+/\d+)", 
        "tipo": "str"},
    "fovea": {
        "regex": r"Fovea:\s*([-\d.,]+)", 
        "tipo": "float"},
    "estrategia": {
        "regex": r"Estratégia:\s*([^\n\r]+)", 
        "tipo": "str"},
    "ght": {
        "regex": r"GHT:\s*([^\n\r]+)", 
        "tipo": "str"},
    "vqi": {
        "regex": r"VQi:\s*([\d.,]+)", 
        "tipo": "float"},
    "md": {
        "regex": r"MDh:\s*([-\d.,]+)", 
        "tipo": "float"},
    "psd": {
        "regex": r"PSD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "cpsd": {
        "regex": r"CPSD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "sfh": {
        "regex": r"SFh:\s*([-\d.,]+)", 
        "tipo": "float"},
    "ms": {
        "regex": r"MS:\s*([-\d.,]+)", 
        "tipo": "float"}
}


def calcular_percentual(valor):
    try:
        if valor is None: 
            return None
        
        valor = str(valor).strip()

        if "/" in valor:
            numerador, denominador = map(int, valor.split("/"))
            return (numerador / denominador) * 100 if denominador != 0 else None
        
        return float(valor.replace("%", "").replace(",", "."))
    
    except (ValueError, ZeroDivisionError, AttributeError):
        return None

def _classificar_escala_100(campo_valor):

    if campo_valor is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(campo_valor))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= 95.0: 
        return "preservado"
    
    if valor >= 80.0: 
        return "leve"
    
    if valor >= 50.0: 
        return "moderado"
    
    return "avancado"


def classificar_erros_fixacao(erros_fixacao):

    percentual = calcular_percentual(erros_fixacao)

    if percentual is None: 
        return "não disponível"
    
    if percentual <= 20.0: 
        return "boa"
    
    if percentual <= 33.0: 
        return "moderada"
    
    return "ruim"

def classificar_falsos_positivos(falsos_positivos):

    percentual = calcular_percentual(falsos_positivos)

    if percentual is None: 
        return "normal"
    
    if percentual <= 15.0: 
        return "normal"
    
    if percentual <= 20.0: 
        return "atencao"
    
    return "ruim"

def classificar_falsos_negativos(falsos_negativos):

    percentual = calcular_percentual(falsos_negativos)

    if percentual is None: 
        return "normal"
    
    if percentual <= 15.0: 
        return "normal"
    
    if percentual <= 25.0: 
        return "atencao"
    
    return "ruim"

def classificar_fovea(fovea):

    if fovea is None: 
        return "não disponível"
    
    match = re.search(r"\d+", str(fovea))

    if not match: 
        return "não disponível"
    
    valor = float(match.group())

    if valor >= 30.0: 
        return "normal"
    
    if valor >= 20.0: 
        return "reduzida"
    
    return "muito reduzida"

def classificar_vfi(vfi): 
    return _classificar_escala_100(vfi)

def classificar_vqi(vqi): 
    return _classificar_escala_100(vqi)

def classificar_md(md):

    if md is None: 
        return "não disponível"
    
    match = re.search(r"[-\d.,]+", str(md))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= -2.0: 
        return "normal"
    
    if valor >= -6.0: 
        return "leve"
    
    if valor >= -12.0: 
        return "moderado"
    
    return "grave"

def classificar_mdh(mdh): 
    return classificar_md(mdh)

def classificar_psd(psd):

    if psd is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(psd))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 3.0: 
        return "normal"
    
    if valor < 4.5: 
        return "limítrofe"
    
    return "alterado"

def classificar_cpsd(cpsd):

    if cpsd is None: 
        return "não disponível ou omitido"
    
    match = re.search(r"[\d.,]+", str(cpsd))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 3.0: 
        return "normal"
    
    if valor < 4.5: 
        return "limítrofe"
    
    return "alterado"

def classificar_sfh(sfh):

    if sfh is None: 
        return "não disponível ou omitido"
    
    match = re.search(r"[\d.,]+", str(sfh))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 2.0: 
        return "normal"
    
    if valor <= 3.0: 
        return "limítrofe"
    
    return "elevado"

def classificar_ms(ms):

    if ms is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(ms))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= 26.0: 
        return "preservada"
    
    if valor >= 20.0: 
        return "moderadamente reduzida"
    
    return "severamente reduzida"

def classificar_ght(ght):

    if not ght: 
        return "não disponível"
    
    valor = str(ght).strip().title() 
    
    mapeamento = {
        "Within Normal Limits": "normal",
        "Borderline": "suspeito",
        "Outside Normal Limits": "anormal",
        "General Reduction Of Sensitivity": "depressao generalizada",
        "Abnormally High Sensitivity": "hipersensibilidade"
    }

    return mapeamento.get(valor, "desconhecido")


MAPEAMENTO_CLASSIFICADORES = {
    "fovea": classificar_fovea,
    "vfi": classificar_vfi,
    "md": classificar_md,
    "mdh": classificar_mdh,
    "psd": classificar_psd,
    "erros_fixacao": classificar_erros_fixacao,
    "false_pos": classificar_falsos_positivos,
    "false_neg": classificar_falsos_negativos,
    "vqi": classificar_vqi,
    "cpsd": classificar_cpsd,
    "sfh": classificar_sfh,
    "ms": classificar_ms,
    "ght": classificar_ght
}



def extrair_campos(texto, campos):

    dados = {}

    for nome, config in campos.items(): 
        match = re.search(config["regex"], texto)
        if not match: continue 

        valor = match.group(1)

        if config["tipo"] == "float":
            valor = re.sub(r'[^0-9,.-]', '', valor)
            valor = float(valor.replace(',', '.'))

        elif config["tipo"] == "int":
            valor = int(re.sub(r'[^0-9]', '', valor))

        elif config["tipo"] == "str":
            valor = valor.strip()
        
        dados[nome] = valor 

        if nome in MAPEAMENTO_CLASSIFICADORES:

            funcao_classificadora = MAPEAMENTO_CLASSIFICADORES[nome]
            chave_classificacao = f"{nome}_classificacao"
            dados[chave_classificacao] = funcao_classificadora(valor)

    return dados

def detectar_tipo_exame(texto):

    texto = texto.lower().replace("\n", " ")

    if re.search(r'center\s*24-2\s*threshold', texto): 
        return "humphrey"
    
    if re.search(r'c\s*-?\s*24.*avan', texto): 
        return "optopol"
    
    return "desconhecido"

def extrair_humphrey(texto):

    dados = extrair_campos(texto, CAMPOS_HUMPHREY)

    if dados.get("olho") == "Right": 
        dados["olho"] = "OD"

    elif dados.get("olho") == "Left": 
        dados["olho"] = "OE"

    return dados

def extrair_optopol(texto):
    return extrair_campos(texto, CAMPOS_OPTOPOL)

def estruturar_exame(texto):

    tipo = detectar_tipo_exame(texto)

    if tipo == "humphrey": 
        dados = extrair_humphrey(texto)

    elif tipo == "optopol": 
        dados = extrair_optopol(texto)

    else: 
        dados = {"texto_bruto": texto}

    dados["tipo"] = tipo

    return dados


def extrair_texto_laudo(doc, laudos_texto_folder, paciente):

    num_paginas = len(doc)

    text = doc[num_paginas-1].get_text()

    text_path = os.path.join(laudos_texto_folder, f"{paciente}_laudo.txt")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

def extrair_texto_exame(doc, paginas_exame):

    exames = []

    for i, pagina in enumerate(paginas_exame, start=1):

        text = doc[pagina - 1].get_text().replace("：", ":").replace("％", "%")

        dados = estruturar_exame(text)

        exames.append({"exame": i, "dados": dados})

    return exames

def salvar_json_exames(exames, paciente, exames_json_folder):

    dados = {paciente: {"exames": exames}}

    json_path = os.path.join(exames_json_folder, f"{paciente}.json")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)