import pdfplumber
import os
import glob
import json
import pandas as pd
from datetime import datetime

PASTA_ENTRADA = "calculadoras"
ARQUIVO_SAIDA_EXCEL = "output/relatorio_final.xlsx"
ARQUIVO_SAIDA_CSV = "output/relatorio_final.csv"
ARQUIVO_SAIDA_JSON = "output/dados_extraidos.json"
ARQUIVO_LOG = "output/log_processamento.txt"


def extrair_dados_direto(caminho_pdf):
    mapa_campos = {
        "Contrato": (105, 100, 200, 140),
        "CPF_CNPJ": (285, 100, 400, 140),
        "Nome_Razao": (105, 140, 430, 175),
        "Chassi": (285, 180, 430, 200),
        "Placa": (518, 180, 590, 200),
        "Escob": (480, 320, 590, 360),
        "Marca": (285, 380, 400, 400),
        "Modelo": (285, 400, 590, 420),
        "Ano_Modelo": (105, 440, 140, 460),
        "Ano_Fabricacao": (285, 440, 320, 460),
        "Codigo_FIPE": (105, 480, 200, 500),
        "Cor": (285, 480, 380, 500),
        "Valor_FIPE": (480, 480, 590, 500),
        "Tipo_Acao": (105, 1060, 200, 1100),
        "Total_Debitos": (105, 1100, 200, 1140),
        "CEP": (105, 1520, 200, 1540),
        "Endereço": (105, 1540, 380, 1580),
        "Bairro": (285, 1520, 590, 1540),
        "Número": (480, 1540, 590, 1580),
        "Complemento": (105, 1580, 590, 1600),
        "Município": (285, 1380, 590, 1400),
        "UF": (105, 1380, 200, 1400),
    }

    dados_finais = {}

    dados_finais["Arquivo_Origem"] = os.path.basename(caminho_pdf)

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            pagina = pdf.pages[0]
            largura_pag = pagina.width

            for chave, area in mapa_campos.items():
                try:
                    if area[2] > largura_pag:
                        dados_finais[chave] = (
                            f"ERRO: Coordenada x1 ({area[2]}) > Largura ({largura_pag})"
                        )
                        continue

                    recorte = pagina.crop(area)
                    texto = recorte.extract_text()

                    if texto:
                        dados_finais[chave] = texto.replace("\n", " ").strip()
                    else:
                        dados_finais[chave] = ""

                except Exception as e:
                    dados_finais[chave] = f"Erro leitura: {str(e)}"

    except Exception as e:
        print(f"Erro fatal ao abrir {caminho_pdf}: {e}")
        return None

    return dados_finais


def salvar_log(lista_mensagens):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
        f.write(f"--- LOG DE PROCESSAMENTO: {timestamp} ---\n\n")
        for msg in lista_mensagens:
            f.write(msg + "\n")
    print(f"[OK] Log salvo em: {ARQUIVO_LOG}")


def salvar_json(lista_dados):
    with open(ARQUIVO_SAIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(lista_dados, f, indent=4, ensure_ascii=False)
    print(f"[OK] JSON salvo em: {ARQUIVO_SAIDA_JSON}")


def salvar_excel_csv(lista_dados):
    if not lista_dados:
        print("Nenhum dado para salvar no Excel.")
        return

    df = pd.DataFrame(lista_dados)

    df.to_excel(ARQUIVO_SAIDA_EXCEL, index=False)
    print(f"[OK] Excel salvo em: {ARQUIVO_SAIDA_EXCEL}")

    df.to_csv(ARQUIVO_SAIDA_CSV, index=False, sep=",", encoding="utf-8-sig")
    print(f"[OK] CSV salvo em: {ARQUIVO_SAIDA_CSV}")


def main():
    if not os.path.exists(PASTA_ENTRADA):
        print(
            f"ERRO: Pasta '{PASTA_ENTRADA}' não encontrada. Crie a pasta e coloque os PDFs."
        )
        return
    arquivos_pdf = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))

    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado na pasta '{PASTA_ENTRADA}'.")
        return

    print(f"Encontrados {len(arquivos_pdf)} arquivos para processar.\n")

    todos_dados = []
    log_msgs = []

    for i, arquivo in enumerate(arquivos_pdf):
        nome_arq = os.path.basename(arquivo)
        print(f"Processando [{i+1}/{len(arquivos_pdf)}]: {nome_arq}...")

        dados = extrair_dados_direto(arquivo)

        if dados:
            todos_dados.append(dados)
            log_msgs.append(
                f"SUCESSO: {nome_arq} - Contrato: {dados.get('Contrato', 'N/A')}"
            )
        else:
            log_msgs.append(f"FALHA: {nome_arq} - Arquivo corrompido ou ilegível.")
    print("\n--- Salvando Arquivos ---")
    salvar_json(todos_dados)
    salvar_excel_csv(todos_dados)
    salvar_log(log_msgs)

    print("\nPROCESSO CONCLUÍDO COM SUCESSO!")


if __name__ == "__main__":
    main()
