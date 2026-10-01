# Trabalho I — Comparação de Serviços de Inteligência Artificial em Nuvem

**Disciplina:** Computação em Nuvem

**Integrantes:**
1. JOÃO DAVID DE FREITAS CESÁRIO
2. SÉRGIO MAIA RAULINO
3. ANA PAULA SILVA DE ARAUJO

**Etapa:** 1 — Análise Comparativa

**Data de consulta das informações:** 30/09/2026

---

# 1. Introdução

Os principais provedores de computação em nuvem disponibilizam serviços de Inteligência Artificial que podem ser incorporados a aplicações por meio de APIs e SDKs, permitindo que desenvolvedores utilizem funcionalidades de IA sem a necessidade de desenvolver, treinar e operar modelos próprios.

Este trabalho realiza uma análise comparativa de serviços de Inteligência Artificial oferecidos pela Amazon Web Services (AWS), Microsoft Azure e Google Cloud, considerando tanto aspectos técnicos quanto econômicos.

A análise foi organizada em três categorias de funcionalidades:

1. Processamento de Linguagem Natural, com foco em análise de sentimento;
2. Análise de imagens, com foco em detecção e classificação de conteúdo visual;
3. Análise e extração de documentos, com foco em OCR, formulários, tabelas e informações estruturadas.

A escolha dessas categorias foi motivada pela diversidade das modalidades de dados processadas — texto, imagem e documentos — e pela existência de serviços comparáveis entre os três provedores.

---

# 2. Seleção dos Serviços

## 2.1 Critérios de seleção

A seleção das categorias considerou os seguintes critérios:

- existência de serviços equivalentes em pelo menos dois dos três provedores;
- disponibilidade de acesso programático por API e/ou SDK;
- relevância para o desenvolvimento de aplicações;
- diversidade funcional, evitando concentrar a análise em um único domínio;
- possibilidade de comparar parâmetros de entrada, resultados, limitações e modelos de cobrança;
- possibilidade de utilização posterior dos serviços em experimentos práticos.

O objetivo não é estabelecer um único serviço como superior aos demais, mas identificar diferenças e trade-offs relevantes para desenvolvedores.

## 2.2 Categorias e serviços selecionados

| Categoria | AWS | Google Cloud | Microsoft Azure |
|---|---|---|---|
| Processamento de Linguagem Natural — análise de sentimento | Amazon Comprehend | Cloud Natural Language | Azure AI Language |
| Análise de imagens | Amazon Rekognition | Cloud Vision API | Azure AI Vision — Image Analysis |
| Análise e extração de documentos | Amazon Textract | Document AI — Form Parser | Azure AI Document Intelligence |

Sempre que identificados serviços equivalentes nos três provedores, os três foram incluídos na comparação.

---

# 3. Processamento de Linguagem Natural — Análise de Sentimento

## 3.1 Visão geral

A análise de sentimento procura identificar a orientação emocional ou opinativa presente em um texto. Os três provedores oferecem uma funcionalidade diretamente relacionada a essa tarefa, embora utilizem representações diferentes para seus resultados.

Os serviços comparados são:

- **AWS:** Amazon Comprehend;
- **Google Cloud:** Cloud Natural Language;
- **Microsoft Azure:** Azure AI Language.

---

## 3.2 Amazon Comprehend

O Amazon Comprehend oferece diversas funcionalidades de processamento de linguagem natural, incluindo análise de sentimento, reconhecimento de entidades, extração de frases-chave, análise sintática e detecção de idioma.

Para análise de sentimento, a operação principal utilizada nesta comparação é `DetectSentiment`.

A requisição possui, entre outros elementos, os campos:

- `LanguageCode`: idioma do documento;
- `Text`: texto a ser analisado.

A documentação atual informa que `Text` é uma string UTF-8 com tamanho máximo de 5 KB. Os idiomas primários aceitos incluem, entre outros, inglês, espanhol, francês, alemão, italiano e português.

A resposta apresenta o sentimento predominante entre:

- `POSITIVE`
- `NEGATIVE`
- `NEUTRAL`
- `MIXED`

Além do rótulo, a resposta apresenta uma pontuação para cada classe.

### Exemplo de utilização

```python
import boto3

client = boto3.client("comprehend", region_name="us-east-1")

response = client.detect_sentiment(
    Text="This movie was excellent.",
    LanguageCode="en"
)

print(response["Sentiment"])
print(response["SentimentScore"])

```

O SDK utilizado no exemplo é o `boto3`. O código acima é ilustrativo e foi adaptado da documentação oficial do Amazon Comprehend.

### Características relevantes

| Aspecto | Amazon Comprehend |
| :--- | :--- |
| **Operação** | DetectSentiment |
| **Entrada principal** | Texto UTF-8 |
| **Idioma** | Informado explicitamente |
| **Tamanho máximo do texto** | 5 KB |
| **Classes** | Positive, Negative, Neutral, Mixed |
| **Resultado** | Classe + scores |
| **API** | REST |
| **SDK** | AWS SDK / boto3 |
| **Autenticação** | Credenciais AWS / IAM |

**Limitação relevante:** O limite de 5 KB por texto deve ser considerado por aplicações que processem documentos longos ou grandes avaliações textuais. Para experimentos comparativos, esse limite precisa ser levado em conta para garantir que as mesmas entradas sejam submetidas aos três provedores.

---

## 3.3 Google Cloud Natural Language

O Cloud Natural Language oferece funcionalidades de compreensão de linguagem natural, incluindo análise de entidades, análise de sentimento, sentimento associado a entidades, análise sintática, classificação de conteúdo e moderação.
A análise de sentimento é realizada por meio do método `analyzeSentiment`.

A API aceita um objeto Document contendo:
* Tipo do documento;
* Idioma (opcionalmente);
* Conteúdo textual ou URI de um objeto no Google Cloud Storage.

São aceitos documentos de texto simples (`PLAIN_TEXT`) e HTML. Diferentemente do Amazon Comprehend, o Google não representa o resultado principal somente como uma classe categórica. O resultado de sentimento contém:
* **score**: valor de -1,0 a +1,0;
* **magnitude**: valor não negativo que representa a intensidade agregada do sentimento.

O *score* positivo representa orientação positiva, enquanto valores negativos representam orientação negativa. A resposta também pode fornecer o sentimento individual de cada sentença.

### Exemplo de utilização

```python
from google.cloud import language_v2

client = language_v2.LanguageServiceClient()
document = language_v2.Document(
    content="This movie was excellent.",
    type_=language_v2.Document.Type.PLAIN_TEXT,
    language_code="en"
)

response = client.analyze_sentiment(
    request={"document": document}
)

print(response.document_sentiment.score)
print(response.document_sentiment.magnitude)
```

O SDK é disponibilizado pela biblioteca oficial `google-cloud-language`.

### Características relevantes

| Aspecto | Cloud Natural Language |
| :--- | :--- |
| **Operação** | analyzeSentiment |
| **Entrada principal** | Documento textual |
| **Formatos** | Texto simples e HTML |
| **Idioma** | Informado ou detectado automaticamente |
| **Resultado** | score + magnitude |
| **Intervalo do score** | -1,0 a +1,0 |
| **Resultado por sentença** | Sim |
| **API** | REST |
| **SDK** | Google Cloud client libraries |
| **Autenticação** | Application Default Credentials / OAuth |

Uma diferença importante em relação ao AWS Comprehend é a representação do sentimento: o Google fornece um valor contínuo, em vez de limitar a resposta principal a quatro classes.

---

## 3.4 Azure AI Language

O Azure AI Language oferece funcionalidades para compreensão de textos, incluindo análise de sentimento e opinion mining. A operação de análise de sentimento classifica o documento e suas sentenças como:
* positive
* neutral
* negative

Além da classificação, são retornados scores de confiança entre 0 e 1 para cada classe. A API também permite realizar *opinion mining*, associando sentimentos a aspectos específicos do texto.

### Exemplo de utilização

```python
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
key = os.environ["AZURE_LANGUAGE_KEY"]

client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

documents = ["This movie was excellent."]
result = client.analyze_sentiment(documents)

for document in result:
    print(document.sentiment)
    print(document.confidence_scores)
```

O SDK oficial é o `azure-ai-textanalytics`.

### Características relevantes

| Aspecto | Azure AI Language |
| :--- | :--- |
| **Operação** | Sentiment Analysis |
| **Entrada principal** | Texto |
| **Classes** | Positive, Neutral, Negative |
| **Score** | 0 a 1 por classe |
| **Resultado por sentença** | Sim |
| **Opinion mining** | Sim |
| **API** | REST |
| **SDK** | Azure SDK for Python |
| **Autenticação** | Chave ou Microsoft Entra |
| **Limite de documento** | 5.120 caracteres |

A Microsoft informa que a análise de sentimento e opinion mining no Azure Language estão previstas para aposentadoria em 31 de março de 2029, sendo os novos projetos direcionados ao Microsoft Foundry.

---

## 3.5 Comparação técnica — análise de sentimento

| Característica | AWS Comprehend | Google Natural Language | Azure AI Language |
| :--- | :--- | :--- | :--- |
| **Operação principal** | DetectSentiment | analyzeSentiment | Sentiment Analysis |
| **Entrada** | String | Document | String / lista de documentos |
| **Resultado categórico** | Sim | Não diretamente | Sim |
| **Resultado contínuo** | Scores por classe | Score -1 a +1 | Scores 0 a 1 |
| **Sentimento por sentença**| Não como foco principal | Sim | Sim |
| **Opinion mining** | Não nessa operação | Entity Sentiment (op. própria) | Sim |
| **Idioma** | Informado | Informado ou detectado | Informado |
| **Limite relevante** | 5 KB | Limite superior muito maior | 5.120 caracteres |
| **REST** | Sim | Sim | Sim |
| **SDK Python** | boto3 | google-cloud-language | azure-ai-textanalytics |
| **Modelo próprio nec.** | Não | Não | Não |

**Principal diferença conceitual:**
Embora as três alternativas implementem análise de sentimento, as respostas possuem estruturas diferentes:
* **AWS:** `sentimento = POSITIVE` | `probabilidades = {positive, negative, neutral, mixed}`
* **Google:** `score = 0.8` | `magnitude = 0.8`
* **Azure:** `sentimento = positive` | `scores = {positive, neutral, negative}`

Essa diferença deverá ser considerada em uma futura comparação experimental, pois a saída nativa de cada serviço não possui a mesma representação.

---

# 4. Análise de Imagens

## 4.1 Escopo
Para evitar uma comparação excessivamente ampla, a categoria foi delimitada para detecção e classificação de conteúdo visual, considerando principalmente rótulos/tags e objetos. Os serviços comparados são:
* Amazon Rekognition
* Google Cloud Vision API
* Azure AI Vision — Image Analysis

## 4.2 Amazon Rekognition
O Amazon Rekognition oferece análise automática de imagens e vídeos. Para esta comparação, a operação principal é `DetectLabels`, capaz de detectar objetos, conceitos e cenas presentes em uma imagem.
A entrada pode ser fornecida por:
* Bytes da imagem;
* Objeto armazenado no Amazon S3.

Para a operação de detecção de rótulos, imagens JPEG e PNG são suportadas. Entre os parâmetros importantes estão:
* **MaxLabels**: limita a quantidade de rótulos retornados;
* **MinConfidence**: define a confiança mínima para que um rótulo seja retornado (quando não especificado, o valor padrão é 55%).

### Exemplo

```python
import boto3

client = boto3.client("rekognition", region_name="us-east-1")
response = client.detect_labels(
    Image={
        "S3Object": {
            "Bucket": "meu-bucket",
            "Name": "imagem.jpg"
        }
    },
    MaxLabels=10,
    MinConfidence=80
)

for label in response["Labels"]:
    print(label["Name"], label["Confidence"])
```

### Características

| Aspecto | Amazon Rekognition |
| :--- | :--- |
| **Operação** | DetectLabels |
| **Entrada** | JPEG/PNG, bytes ou S3 |
| **Resultado** | Labels e confiança |
| **Objetos** | Sim |
| **Bounding boxes** | Disponíveis para objetos quando aplicável |
| **Parâmetros** | MaxLabels, MinConfidence |
| **API / SDK** | REST / boto3 |

## 4.3 Google Cloud Vision API
A Cloud Vision API oferece diferentes tipos de análise visual. Para esta categoria foram considerados principalmente:
* `LABEL_DETECTION`
* `OBJECT_LOCALIZATION`

O cliente pode solicitar múltiplas funcionalidades na mesma requisição e limitar a quantidade de resultados por meio de `maxResults`. O Google também permite selecionar modelos como `builtin/stable` ou `builtin/latest`, quando aplicável.

### Exemplo

```python
from google.cloud import vision

client = vision.ImageAnnotatorClient()
with open("imagem.jpg", "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.label_detection(image=image)

for label in response.label_annotations:
    print(label.description, label.score)
```

### Características

| Aspecto | Google Cloud Vision |
| :--- | :--- |
| **Operação** | Label Detection / Object Localization |
| **Entrada** | Bytes ou Cloud Storage |
| **Resultado** | Labels, scores e atributos |
| **Objetos** | Sim |
| **Bounding boxes** | Object Localization |
| **Parâmetros** | maxResults |
| **Modelos** | Stable/Latest quando aplicável |
| **API / SDK** | REST / google-cloud-vision |

## 4.4 Azure AI Vision — Image Analysis
O Azure AI Vision Image Analysis permite solicitar diferentes características visuais através da API de análise. Entre os recursos disponíveis estão: tags, objects, OCR (Read), people, captions, dense captions e smart crops.
Para a comparação principal foram considerados **tags** e **objects**.

A API pode receber uma URL pública ou os bytes da imagem. O SDK oficial para Python é `azure-ai-vision-imageanalysis`.

### Exemplo

```python
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

client = ImageAnalysisClient(
    endpoint=os.environ["VISION_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["VISION_KEY"])
)

with open("imagem.jpg", "rb") as f:
    image_data = f.read()

result = client.analyze(
    image_data=image_data,
    visual_features=[
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS
    ]
)

for tag in result.tags.list:
    print(tag.name, tag.confidence)
```

### Características

| Aspecto | Azure AI Vision |
| :--- | :--- |
| **Operação** | Image Analysis |
| **Entrada** | URL ou bytes |
| **Tags / Objetos** | Sim / Sim |
| **Bounding boxes** | Sim para objetos |
| **OCR / Pessoas** | Sim / Sim |
| **Captions** | Sim |
| **API / SDK** | REST / azure-ai-vision-imageanalysis |

**Limitação importante:** A documentação atual informa que o Image Analysis 4.0 do Azure Vision está depreciado e possui aposentadoria prevista para 25 de setembro de 2028. O fato de o serviço ainda estar disponível em 2026 o torna utilizável para esta comparação, mas o ciclo de vida deve ser registrado como uma diferença relevante entre as ofertas.

---

# 5. Análise e Extração de Documentos

## 5.1 Escopo
A terceira categoria concentra-se na extração de informações estruturadas de documentos (OCR, texto, tabelas, pares chave-valor, elementos de seleção e estrutura/layout).
Os serviços selecionados são:
* Amazon Textract
* Google Document AI — Form Parser
* Azure AI Document Intelligence

## 5.2 Amazon Textract
O Amazon Textract analisa documentos e identifica relações entre elementos de texto. As operações de análise podem retornar texto, formulários, tabelas, respostas de consultas, assinaturas e elementos de seleção.
A operação `AnalyzeDocument` utiliza o parâmetro `FeatureTypes` para indicar quais funcionalidades devem ser aplicadas (ex: `TABLES`, `FORMS`, `QUERIES`, `LAYOUT`). A resposta utiliza uma estrutura de objetos `Block`.

### Exemplo

```python
import boto3

client = boto3.client("textract", region_name="us-west-2")
with open("documento.png", "rb") as f:
    document_bytes = f.read()

response = client.analyze_document(
    Document={"Bytes": document_bytes},
    FeatureTypes=["FORMS", "TABLES"]
)

for block in response["Blocks"]:
    print(block["BlockType"])
```

Os formulários são representados principalmente por relações entre objetos `KEY_VALUE_SET`, enquanto tabelas e células também possuem estruturas específicas.

### Características

| Aspecto | Amazon Textract |
| :--- | :--- |
| **Operação** | AnalyzeDocument |
| **Entrada** | Documentos em formatos suportados |
| **Formulários / Tabelas**| Sim / Sim |
| **Key-value pairs** | Sim |
| **Queries / Layout** | Sim / Sim |
| **Resultado** | Estrutura de Block |
| **API síncrona / assínc.**| Sim / Sim |
| **SDK** | boto3 |

## 5.3 Google Document AI — Form Parser
O Form Parser do Google Document AI é um processador pré-treinado voltado à extração de informações de formulários. Ele pode extrair pares chave-valor, tabelas, caixas de seleção, texto, layout e entidades genéricas (e-mail, telefone, URL, data, endereço, pessoa, organização, etc.).
O Form Parser é pré-treinado e não pode ser treinado novamente.

### Exemplo

```python
from google.cloud import documentai

client = documentai.DocumentProcessorServiceClient()
with open("formulario.pdf", "rb") as f:
    content = f.read()

raw_document = documentai.RawDocument(
    content=content,
    mime_type="application/pdf"
)

request = documentai.ProcessRequest(
    name="projects/PROJECT/locations/us/processors/PROCESSOR",
    raw_document=raw_document
)

result = client.process_document(request=request)

for entity in result.document.entities:
    print(entity.type_, entity.mention_text)
```

### Características

| Aspecto | Google Document AI Form Parser |
| :--- | :--- |
| **Tipo** | Processador pré-treinado |
| **KVP / Tabelas** | Sim / Sim |
| **Checkboxes / OCR** | Sim / Sim |
| **Layout / Entidades** | Sim / Sim |
| **Treinamento** | Não (pré-treinado) |
| **API / SDK** | REST / Google Cloud client libraries |

## 5.4 Azure AI Document Intelligence
O Azure AI Document Intelligence fornece análise de documentos e modelos pré-construídos e personalizados. Entre os recursos disponíveis estão: extração de texto, layout, tabelas, pares chave-valor, selection marks, campos estruturados, além de modelos pré-construídos para recibos, invoices, identidades, cartões e contratos.

### Exemplo

```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

client = DocumentIntelligenceClient(
    endpoint=os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOCUMENTINTELLIGENCE_API_KEY"])
)

with open("documento.pdf", "rb") as f:
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=f
    )

result = poller.result()

for page in result.pages:
    print(page.page_number)
    for line in page.lines:
        print(line.content)
```

### Características

| Aspecto | Azure Document Intelligence |
| :--- | :--- |
| **OCR / Layout** | Sim / Sim |
| **Tabelas** | Sim |
| **Key-value pairs** | Dependente do modelo |
| **Selection marks** | Sim |
| **Prebuilt / Custom models**| Sim / Sim |
| **API / SDK** | REST / azure-ai-documentintelligence |

---

# 6. Comparação técnica entre as três categorias

## 6.1 Resumo

| Categoria | AWS | Google Cloud | Azure |
| :--- | :--- | :--- | :--- |
| **Análise de sentimento** | Comprehend | Natural Language | Azure AI Language |
| **Imagens** | Rekognition | Vision API | AI Vision |
| **Documentos** | Textract | Document AI | Document Intelligence |

As três plataformas oferecem mecanismos de acesso por APIs e SDKs, mas apresentam diferenças nas operações, parâmetros, representação dos resultados e limitações. Uma característica comum às três é a utilização de serviços pré-treinados, permitindo incorporar funcionalidade de IA sem que o desenvolvedor precise construir e treinar um modelo próprio.

---

# 7. Análise Econômica

## 7.1 Metodologia
Para permitir comparações diretas, os custos devem ser analisados utilizando cargas equivalentes dentro de cada categoria. As seguintes unidades serão utilizadas:
* **PLN:** quantidade de caracteres processados;
* **Imagens:** número de imagens analisadas;
* **Documentos:** número de páginas processadas.

Os valores apresentados devem ser interpretados como preços de tabela e não como uma estimativa da fatura final de uma aplicação, pois fatores como região, contrato, impostos, armazenamento e serviços auxiliares podem alterar o custo efetivo. *As páginas oficiais foram consultadas em 30/09/2026.*

# 8. Preços — Processamento de Linguagem Natural

**AWS Comprehend**
A cobrança é baseada em unidades de 100 caracteres, com cobrança mínima de três unidades (300 caracteres) por solicitação.
* Primeiro intervalo: US$ 0,0001 por unidade de 100 caracteres.
* Franquia: 50.000 unidades de texto (5 milhões de caracteres/mês) no Free Tier.
* Fonte: [Amazon Comprehend Pricing](https://aws.amazon.com/comprehend/pricing/)

**Google Cloud Natural Language**
Cobrança baseada no número de caracteres Unicode processados (unidades de 1.000 caracteres).
* 0 a 5.000 unidades/mês: gratuitas
* 5.001 a 1.000.000: US$ 1,00 por 1.000 caracteres
* 1.000.001 a 5.000.000: US$ 0,50 por 1.000 caracteres
* Acima de 5.000.000: US$ 0,25 por 1.000 caracteres
* Fonte: [Cloud Natural Language Pricing](https://cloud.google.com/products/natural-language/pricing)

**Azure AI Language**
Utiliza *Text Records* (até 1.000 caracteres por registro).
* Franquia: 5.000 Text Records gratuitos por mês compartilhados entre as funcionalidades.
* Fonte: [Azure Language Pricing](https://azure.microsoft.com/pt-br/pricing/details/language/)

# 9. Preços — Análise de Imagens

**AWS Rekognition**
Para `DetectLabels`: US$ 0,001 por imagem (no primeiro milhão de imagens mensais).
* Exemplo (10.000 imagens): 10.000 × US$ 0,001 = **US$ 10,00**
* Fonte: [Amazon Rekognition Pricing](https://aws.amazon.com/rekognition/pricing/)

**Google Cloud Vision**
Para `Label Detection`:
* Primeiras 1.000 unidades/mês: gratuitas
* 1.001 a 5.000.000: US$ 1,50 por 1.000 imagens
* Exemplo (10.000 imagens, descontando franquia): 9 × US$ 1,50 = **US$ 13,50**
* Fonte: [Cloud Vision API Pricing](https://cloud.google.com/vision/pricing)

**Azure AI Vision**
* Franquia: 5.000 transações por mês gratuitas.
* O tier Standard cobra por transações conforme a região.
* Fonte: [Azure Vision Pricing](https://azure.microsoft.com/pt-br/pricing/details/computer-vision/)

# 10. Preços — Documentos

**AWS Textract**
Para a operação `AnalyzeDocument` (região US West - Oregon):
* Tables: US$ 0,015 por página
* Forms: US$ 0,05 por página
* Juntos: US$ 0,065 por página
* Exemplo (10.000 páginas conjuntas): 10.000 × US$ 0,065 = **US$ 650,00**
* Fonte: [Amazon Textract Pricing](https://aws.amazon.com/textract/pricing/)

**Google Document AI — Form Parser**
Cobrança de US$ 30 por 1.000 páginas (na faixa até 1 milhão).
* Exemplo (10.000 páginas): 10 × US$ 30 = **US$ 300,00**
* Fonte: [Document AI Pricing](https://cloud.google.com/products/document-ai/pricing)

**Azure AI Document Intelligence**
* Franquia: Até 500 páginas por mês gratuitas.
* Modelos cobrados por páginas processadas dependendo da configuração/região.
* Fonte: [Azure Document Intelligence Pricing](https://azure.microsoft.com/pt-br/pricing/details/document-intelligence/)

---

# 11. Síntese Comparativa

## 11.1 Processamento de Linguagem Natural
Os três provedores oferecem funcionalidade equivalente, mas representam os resultados de forma diferente (AWS = categórica com probabilidades; Google = numérica contínua; Azure = categórica e scores de confiança). Isso exige uma camada de normalização caso o desenvolvedor deseje trocar de provedor. Limites de entrada também variam.

## 11.2 Análise de imagens
A AWS (Rekognition) possui parâmetros explícitos para limitar resultados, o Google (Vision) separa tipos de análise na API, e o Azure (Vision) concentra tudo em uma API de `Image Analysis` (atualmente marcada como *deprecated*, o que é um ponto de atenção no ciclo de vida da aplicação).

## 11.3 Análise de documentos
Os provedores extraem dados estruturados, mas de formas distintas. Textract (AWS) usa objetos `Block`. Form Parser (GCP) tem uma estrutura otimizada diretamente para formulários e entidades. Document Intelligence (Azure) foca bastante em modelos pré-construídos para documentos específicos.

# 12. Trade-offs para o desenvolvimento de aplicações
A escolha não depende apenas da existência da funcionalidade. Fatores decisivos incluem:
* Formato das respostas e limites de entrada;
* Facilidade de integração via SDK e modelo de autenticação;
* Capacidade de personalização e existência de modelos pré-construídos;
* Ciclo de vida do produto (ex: depreciações);
* Unidade de cobrança, franquias gratuitas e dependência de serviços da mesma nuvem (S3, Cloud Storage, Blob).

# 13. Considerações sobre a análise econômica
Cenários base para comparações (armazenados nos arquivos `cenarios.csv`, `precos.csv` e pasta `graficos/`):
* **PLN:** 1.000.000 caracteres processados.
* **Imagens:** 10.000 imagens analisadas.
* **Documentos:** 10.000 páginas processadas.

# 14. Conclusão da Etapa 1
A análise identificou ofertas concorrentes consistentes para NLP, Imagens e Documentos nos três grandes provedores. Embora a funcionalidade base seja parecida, as plataformas diferem drasticamente na estrutura das APIs, parâmetros, formato de resposta e modelos de cobrança. Compreender essas divergências é crucial para evitar *vendor lock-in* (ficar preso a um fornecedor) e otimizar custos. A análise teórica serve como base sólida para avaliações práticas e experimentais.

---

# 15. Referências

**AWS**
* [Amazon Comprehend — DetectSentiment API](https://docs.aws.amazon.com/comprehend/latest/APIReference/API_DetectSentiment.html)
* [Amazon Comprehend Pricing](https://aws.amazon.com/comprehend/pricing/)
* [Amazon Rekognition — DetectLabels](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectLabels.html)
* [Amazon Rekognition Pricing](https://aws.amazon.com/rekognition/pricing/)
* [Amazon Textract — Analyzing Documents](https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html)
* [Amazon Textract Pricing](https://aws.amazon.com/textract/pricing/)

**Google Cloud**
* [Cloud Natural Language — Analyzing Sentiment](https://docs.cloud.google.com/natural-language/docs/analyzing-sentiment)
* [Cloud Natural Language Pricing](https://cloud.google.com/products/natural-language/pricing)
* [Cloud Vision API — Detect labels](https://docs.cloud.google.com/vision/docs/detect-labels-image-client-libraries)
* [Cloud Vision API Pricing](https://cloud.google.com/vision/pricing)
* [Document AI — Form Parser](https://docs.cloud.google.com/document-ai/docs/form-parser)
* [Document AI Pricing](https://cloud.google.com/products/document-ai/pricing)

**Microsoft Azure**
* [Azure AI Language — Sentiment Analysis](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview)
* [Azure Language Pricing](https://azure.microsoft.com/pt-br/pricing/details/language/)
* [Azure AI Vision — Image Analysis](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis)
* [Azure Vision Pricing](https://azure.microsoft.com/pt-br/pricing/details/computer-vision/)
* [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview)
* [Azure Document Intelligence Pricing](https://azure.microsoft.com/pt-br/pricing/details/document-intelligence/)

---

# 16. Arquivos complementares

Os exemplos de código utilizados nesta análise estão organizados no diretório `codigo_exemplos/`:
* `codigo_exemplos/nlp/`
* `codigo_exemplos/visao/`
* `codigo_exemplos/documentos/`

Os dados utilizados na análise econômica estão em:
* `analise_economica/precos.csv`
* `analise_economica/cenarios.csv`
