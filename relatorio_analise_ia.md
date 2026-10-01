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



