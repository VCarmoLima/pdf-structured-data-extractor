# PDF Coordinate Extractor

Ferramenta em Python para extração de dados estruturados de arquivos PDF padronizados utilizando mapeamento de coordenadas (X, Y).

Este projeto foi desenvolvido para automatizar a leitura de documentos onde o layout é fixo, mas o OCR tradicional falha ou é desnecessário. Inclui uma ferramenta visual para criar o "gabarito" das coordenadas.

## Funcionalidades

1.  **Mapeador Visual (`mapping_pdf.py`):**
    * Gera uma imagem do PDF com uma régua/grade sobreposta.
    * Facilita a identificação das coordenadas `(x0, top, x1, bottom)` para configuração.
2.  **Extrator em Lote (`main.py`):**
    * Processa todos os PDFs de uma pasta.
    * Extrai campos específicos (ex: Contrato, CPF, Placa, Valores).
    * Exporta os dados para Excel (.xlsx), CSV e JSON.
    * Gera logs detalhados de sucesso/erro.

## Nota sobre LGPD e Privacidade

**Este repositório contém apenas o código fonte.**
Os arquivos PDF de entrada (denominados "calculadoras") e os relatórios gerados **não estão incluídos** para proteger dados sensíveis e estar em conformidade com a LGPD (Lei Geral de Proteção de Dados), pois contêm informações pessoais como CPF, nomes e endereços.

Para testar, utilize seus próprios PDFs e ajuste as coordenadas no dicionário `mapa_campos` dentro do arquivo `main.py`.

## Como usar

### 1. Instalação
```bash
pip install -r requirements.txt
```
### 2. Mapeando um novo layout
Edite o arquivo mapear_pdf.py com o caminho do seu PDF alvo e execute:

```bash
python mapping_pdf.py
```

Isso gerará uma imagem gabarito_final.png que ajudará você a descobrir as coordenadas dos campos.

### 3. Executando a extração
Coloque seus arquivos .pdf na pasta calculadoras/.

Execute o script principal:

```bash
python main.py
```
Os resultados serão gerados na raiz (ou pasta output) como relatorio_final.xlsx.

---

## Tecnologias

pdfplumber - Leitura de PDF e extração de texto por área.

Pandas - Manipulação de dados e exportação para Excel.

Pillow (PIL) - Manipulação de imagem para desenhar o gabarito.