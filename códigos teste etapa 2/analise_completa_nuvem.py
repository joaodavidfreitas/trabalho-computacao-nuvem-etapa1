"""
Avaliação de APIs Comerciais de PLN em Nuvem (GCP e Azure)
Disciplina: Ambientes em nuvem para ciência de dados e inteligência artificial
Instituição: Universidade de Fortaleza (Unifor)
Autores: João David de Freitas Cesário, Sérgio Maia Raulino, Ana Paula Silva de Araujo

Este script reproduz o pipeline completo de ablação (com contexto vs sem contexto),
consumo das APIs em nuvem, normalização dos dados e geração das matrizes de confusão.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from google.cloud import language_v2
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from sklearn.metrics import accuracy_score, confusion_matrix

# ==========================================
# 1. CREDENCIAIS SEGURAS (VARIÁVEIS DE AMBIENTE)
# ==========================================
# As chaves devem estar configuradas no SO para execução deste script.
AZURE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT", "COLE_O_ENDPOINT_AQUI")
AZURE_KEY = os.getenv("AZURE_LANGUAGE_KEY", "COLE_A_CHAVE_AQUI")
# GCP usa: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/caminho/para/chave.json"

try:
    gcp_client = language_v2.LanguageServiceClient()
    azure_client = TextAnalyticsClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_KEY)
    )
except Exception as e:
    print(f"⚠️ Aviso: Configure as credenciais no ambiente para executar chamadas reais. Detalhe: {e}")


# ==========================================
# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==========================================
print("Carregando dataset 'ramondomiingos/ptbr-irony-idioms-regionalism'...")
dataset = load_dataset("ramondomiingos/ptbr-irony-idioms-regionalism", split="train")
df = dataset.to_pandas()

def extrair_frase_sem_contexto(texto):
    """Extrai estritamente a fala entre aspas, removendo o contexto."""
    match = re.search(r"['\"](.*?)['\"]", str(texto))
    return match.group(1) if match else texto

df['Frase_Isolada'] = df['Texto de Entrada'].apply(extrair_frase_sem_contexto)


# ==========================================
# 3. FUNÇÕES DE CHAMADA ÀS APIs
# ==========================================
def analisar_azure(texto):
    try:
        docs = [{"id": "1", "language": "pt", "text": str(texto)[:5000]}]
        response = azure_client.analyze_sentiment(documents=docs)[0]
        return response.sentiment
    except Exception as e:
        return "error"

def analisar_gcp(texto):
    try:
        doc = language_v2.Document(content=str(texto), type_=language_v2.Document.Type.PLAIN_TEXT, language_code="pt")
        response = gcp_client.analyze_sentiment(request={"document": doc})
        return response.document_sentiment.score
    except Exception as e:
        return None

# Obs: Para não consumir cota na demonstração, assume-se que os dados
# brutos já foram coletados e estão sendo carregados dos arquivos CSV.
# O processamento real em lote usaria:
# df['Azure_Com_Contexto'] = df['Texto de Entrada'].apply(analisar_azure)
# df['Azure_Sem_Contexto'] = df['Frase_Isolada'].apply(analisar_azure)


# ==========================================
# 4. GABARITO OURO E DISCRETIZAÇÃO
# ==========================================
def extrair_gabarito_oficial(metrica):
    texto = str(metrica).lower()
    tags_negativas = ['negativo', 'reclamação', 'irritação', 'crítica', 'frustração', 'mágoa', 'cobrança', 'denúncia', 'problema', 'erro', 'descontentamento', 'insatisfação']
    tags_positivas = ['positivo', 'elogio', 'aprovação', 'sucesso', 'bom', 'tranquilo', 'maravilhoso', 'genial', 'animado', 'aventureiro']
    
    if any(tag in texto for tag in tags_negativas): return 'negative'
    elif any(tag in texto for tag in tags_positivas): return 'positive'
    return 'neutral'

df['Gabarito_Ouro'] = df['Métricas de Sucesso'].apply(extrair_gabarito_oficial)

def classificar_gcp(score):
    if pd.isna(score): return 'neutral'
    if score <= -0.25: return 'negative'
    if score >= 0.25:  return 'positive'
    return 'neutral'

# Simulação de pipeline carregando os arquivos gerados (para plotar gráficos)
try:
    df_azure_full = pd.read_csv('../dados/resultado_azure_completo.csv')
    df_azure_sem = pd.read_csv('../dados/resultado_azure_sem_contexto.csv')
    df_gcp = pd.read_csv('../dados/resultado_gcp_doutorado_completo.csv')
    
    df['Azure_Com_Contexto'] = df_azure_full['Sentimento_Azure'].replace('mixed', 'neutral').str.lower()
    df['Azure_Sem_Contexto'] = df_azure_sem['Azure_Sem_Contexto'].replace('mixed', 'neutral').str.lower()
    df['GCP_Com_Contexto'] = df_gcp['GCP_Score_Com_Contexto'].apply(classificar_gcp)
    df['GCP_Sem_Contexto'] = df_gcp['GCP_Score_Sem_Contexto'].apply(classificar_gcp)
except FileNotFoundError:
    print("Arquivos CSV de cache não encontrados. Pule para a análise caso rodado localmente.")

# ==========================================
# 5. CÁLCULO DE ACURÁCIA E PLOTAGEM
# ==========================================
cenarios = {
    'Azure (Com Contexto)': 'Azure_Com_Contexto',
    'Azure (Sem Contexto)': 'Azure_Sem_Contexto',
    'GCP (Com Contexto)': 'GCP_Com_Contexto',
    'GCP (Sem Contexto)': 'GCP_Sem_Contexto'
}

# Certifica-se de que a pasta de imagens existe
os.makedirs('../imagens', exist_ok=True)

try:
    print("="*50)
    print("COMPARAÇÃO DE ACURÁCIA: GABARITO OFICIAL")
    print("="*50)
    resultados_acuracia = []
    
    for nome, coluna in cenarios.items():
        acuracia = accuracy_score(df['Gabarito_Ouro'], df[coluna])
        resultados_acuracia.append({'Modelo/Cenário': nome, 'Acurácia (%)': round(acuracia * 100, 2)})
        print(f"{nome:.<30} {acuracia * 100:.2f}%")
        
    # --- Gráfico 1: Acurácia ---
    df_plot = pd.DataFrame(resultados_acuracia)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Acurácia (%)', y='Modelo/Cenário', data=df_plot, hue='Modelo/Cenário', palette='viridis', legend=False)
    plt.title('Comparação de Acurácia: GCP vs Azure', fontsize=14)
    plt.xlim(0, 100)
    for index, value in enumerate(df_plot['Acurácia (%)']):
        plt.text(value + 1, index, f'{value}%', va='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('../imagens/grafico_acuracia_gerado.png')
    plt.close()

    # --- Gráfico 2: Matrizes de Confusão ---
    labels = ['negative', 'neutral', 'positive']
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Matrizes de Confusão: Modelos vs Gabarito Ouro', fontsize=16)

    for ax, (nome, coluna) in zip(axes.flatten(), cenarios.items()):
        cm = confusion_matrix(df['Gabarito_Ouro'], df[coluna], labels=labels)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_title(nome)
        ax.set_xlabel('Classificação da Nuvem')
        ax.set_ylabel('Gabarito Oficial')

    plt.tight_layout()
    plt.savefig('../imagens/matrizes_confusao_gerado.png')
    plt.close()
    
    print("\nGráficos gerados com sucesso na pasta '../imagens/'.")

except KeyError as e:
    print("Colunas de resultados pendentes. Rode o processamento da API primeiro.")
