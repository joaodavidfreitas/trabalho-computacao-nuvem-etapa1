# Trabalho I — Comparação de Serviços de IA em Nuvem

**Disciplina:** Computação em Nuvem  
**Integrantes:** JOÃO DAVID DE FREITAS CESÁRIO, SÉRGIO MAIA RAULINO, ANA PAULA SILVA DE ARAUJO  
**Etapa:** 1 — Análise Comparativa | **Data base:** 30/09/2026

---

## 1. Seleção dos Serviços
A análise foca em três categorias com ofertas programáticas (APIs/SDKs) equivalentes nos três principais provedores de nuvem, permitindo avaliar parâmetros, retornos e custos:

| Categoria | AWS | Google Cloud (GCP) | Microsoft Azure |
|---|---|---|---|
| **PLN (Análise de Sentimento)** | Amazon Comprehend | Cloud Natural Language | Azure AI Language |
| **Visão Computacional (Imagens)**| Amazon Rekognition | Cloud Vision API | Azure AI Vision |
| **Extração de Documentos** | Amazon Textract | Document AI (Form Parser) | AI Document Intelligence |

---

## 2. Processamento de Linguagem Natural — Sentimento

### 2.1 Amazon Comprehend
Utiliza a operação `DetectSentiment`. Recebe textos de até 5 KB (UTF-8). Retorna a classe dominante (`POSITIVE`, `NEGATIVE`, `NEUTRAL`, `MIXED`) e suas respectivas probabilidades.

```python
import boto3
client = boto3.client("comprehend", region_name="us-east-1")
response = client.detect_sentiment(Text="This movie was excellent.", LanguageCode="en")
print(response["Sentiment"], response["SentimentScore"])
```

| Aspecto | Amazon Comprehend |
| :--- | :--- |
| **Entrada Máx** | 5 KB |
| **Saída** | Classe categórica + scores de probabilidade |
| **SDK** | `boto3` |

### 2.2 Google Cloud Natural Language
O método `analyzeSentiment` avalia o texto (simples ou HTML) e retorna um resultado contínuo em vez de classes, usando dois eixos principais: `score` (-1,0 a +1,0) e `magnitude`.

```python
from google.cloud import language_v2
client = language_v2.LanguageServiceClient()
doc = language_v2.Document(content="This movie was excellent.", type_=language_v2.Document.Type.PLAIN_TEXT, language_code="en")
response = client.analyze_sentiment(request={"document": doc})
print(f"Score: {response.document_sentiment.score}, Magnitude: {response.document_sentiment.magnitude}")
```

| Aspecto | Cloud Natural Language |
| :--- | :--- |
| **Entrada Máx** | Superior a 5KB (suporta documentos longos) |
| **Saída** | Score (-1 a 1) + Magnitude (numérico) |
| **SDK** | `google-cloud-language` |

### 2.3 Azure AI Language
A operação `Sentiment Analysis` retorna classificações categóricas (`positive`, `neutral`, `negative`) com scores de confiança (0 a 1). Suporta até 5.120 caracteres.

```python
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
client = TextAnalyticsClient(endpoint=os.environ["AZURE_ENDPOINT"], credential=AzureKeyCredential(os.environ["AZURE_KEY"]))
result = client.analyze_sentiment(["This movie was excellent."])
for doc in result: print(doc.sentiment, doc.confidence_scores)
```

| Aspecto | Azure AI Language |
| :--- | :--- |
| **Entrada Máx** | 5.120 caracteres |
| **Saída** | Classe categórica + scores de confiança (0 a 1) |
| **SDK** | `azure-ai-textanalytics` |

---

## 3. Análise de Imagens (Rótulos e Objetos)

### 3.1 Amazon Rekognition
A operação `DetectLabels` identifica objetos e cenas. Permite limitar resultados (`MaxLabels`) e definir confiança mínima (`MinConfidence`).

```python
import boto3
client = boto3.client("rekognition", region_name="us-east-1")
res = client.detect_labels(Image={"S3Object": {"Bucket": "meu-bucket", "Name": "foto.jpg"}}, MaxLabels=10)
for label in res["Labels"]: print(label["Name"], label["Confidence"])
```

### 3.2 Google Cloud Vision API
Utiliza `LABEL_DETECTION` ou `OBJECT_LOCALIZATION`. Permite mesclar várias análises na mesma requisição.

```python
from google.cloud import vision
client = vision.ImageAnnotatorClient()
with open("foto.jpg", "rb") as f: res = client.label_detection(image=vision.Image(content=f.read()))
for label in res.label_annotations: print(label.description, label.score)
```

### 3.3 Azure AI Vision
O SDK acessa a API de Image Analysis. **Nota técnica:** A versão 4.0 está em depreciação (aposentadoria para 2028), indicando transição de arquitetura na Microsoft.

```python
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
client = ImageAnalysisClient(endpoint=os.environ["ENDPOINT"], credential=AzureKeyCredential(os.environ["KEY"]))
with open("foto.jpg", "rb") as f: res = client.analyze(image_data=f.read(), visual_features=[VisualFeatures.TAGS])
for tag in res.tags.list: print(tag.name, tag.confidence)
```

---

## 4. Análise e Extração de Documentos

### 4.1 Amazon Textract
A API `AnalyzeDocument` extrai textos, tabelas e formulários estruturando o retorno em objetos do tipo `Block` (ex: `KEY_VALUE_SET`).

```python
import boto3
client = boto3.client("textract", region_name="us-west-2")
with open("doc.png", "rb") as f: res = client.analyze_document(Document={"Bytes": f.read()}, FeatureTypes=["FORMS", "TABLES"])
for block in res["Blocks"]: print(block["BlockType"])
```

### 4.2 Google Document AI (Form Parser)
Processador pré-treinado nativamente estruturado para extrair entidades específicas de formulários, tabelas e caixas de seleção.

```python
from google.cloud import documentai
client = documentai.DocumentProcessorServiceClient()
with open("doc.pdf", "rb") as f: req = documentai.ProcessRequest(name="projects/PROJ/locations/us/processors/PROC", raw_document=documentai.RawDocument(content=f.read(), mime_type="application/pdf"))
res = client.process_document(request=req)
for entity in res.document.entities: print(entity.type_, entity.mention_text)
```

### 4.3 Azure AI Document Intelligence
Oferece forte foco em modelos pré-construídos para documentos específicos (recibos, identidades) ou análise genérica de layout/estrutura.

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
client = DocumentIntelligenceClient(endpoint=os.environ["ENDPOINT"], credential=AzureKeyCredential(os.environ["KEY"]))
with open("doc.pdf", "rb") as f: res = client.begin_analyze_document("prebuilt-layout", body=f).result()
for page in res.pages: print(page.page_number)
```

---

## 5. Análise Econômica
*Preços baseados nas tabelas oficiais consultadas na região US-East/West. Desconsidera-se as camadas gratuitas para fins de simulação de carga empresarial.*

### 5.1 PLN (Cenário: 1 milhão de caracteres/mês)
* **AWS:** Cobrado a US$ 0,0001 por bloco de 100 caracteres.
* **GCP:** US$ 1,00 a cada 1.000 caracteres processados.
* **Azure:** Medido em *Text Records* (blocos de 1.000 caracteres).

### 5.2 Imagens (Cenário: 10.000 imagens/mês)
* **AWS:** US$ 0,001 por imagem. **Custo:** 10.000 × US$ 0,001 = **US$ 10,00**
* **GCP:** US$ 1,50 por 1.000 imagens. **Custo:** 10 × US$ 1,50 = **US$ 15,00**
* **Azure:** Baseado em transações (Standard tier) dependendo dos *features* visuais solicitados.

### 5.3 Documentos (Cenário: 10.000 páginas/mês)
* **AWS:** Tabelas ($0,015) + Forms ($0,05). **Custo:** 10.000 × $0,065 = **US$ 650,00**
* **GCP:** US$ 30,00 por 1.000 páginas. **Custo:** 10 × $30 = **US$ 300,00**
* **Azure:** Varia conforme o modelo pré-construído acionado (Layout vs. Invoice).

---

## 6. Síntese Comparativa e Conclusões
As três plataformas oferecem as mesmas capacidades fundamentais de IA, mas com arquiteturas e *trade-offs* distintos:

1. **Retorno de Dados:** A maior barreira de migração (*vendor lock-in*) está na estrutura dos dados. Migrar do AWS Comprehend para o Google Natural Language exige reescrever a lógica, pois um retorna rótulos e o outro retorna um eixo cartesiano (score/magnitude).
2. **Limitações de Payload:** Azure e AWS possuem restrições mais rígidas de KB/caracteres por requisição na API de texto em comparação ao Google Cloud.
3. **Custos:** O faturamento varia severamente na extração de documentos, onde a escolha exata das *features* (Tabelas vs. OCR puro) dita o custo na AWS, enquanto o Google adota um valor flat de US$ 30/1k páginas para seu processador de formulários.
4. **Ciclo de vida:** É vital atentar-se a depreciações (ex: Azure Vision 4.0), que podem exigir refatoração prematura da aplicação.

## 7. Referências e Arquivos
* Documentação Oficial de Preços e APIs AWS, GCP e Azure (Setembro/2026).
* Códigos e planilhas de cenários consolidadas nas pastas `/codigo_exemplos` e `/analise_economica` deste repositório.
