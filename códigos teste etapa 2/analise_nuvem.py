"""
Avaliação de APIs Comerciais de PLN em Nuvem (GCP e Azure)
Disciplina: Ambientes em nuvem para ciência de dados e inteligência artificial
Instituição: Universidade de Fortaleza (Unifor)
Autores: João David de Freitas Cesário, Sérgio Maia Raulino, Ana Paula Silva de Araujo
"""

import os
import re
import pandas as pd
from datasets import load_dataset
from google.cloud import language_v2
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# ==========================================
# 1. CREDENCIAIS SEGURAS (VIA VARIÁVEIS DE AMBIENTE)
# ==========================================
# Atenção Professor/Avaliador: As chaves não estão expostas no código. 
# É necessário configurar as variáveis de ambiente localmente para testar.
AZURE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT", "COLE_O_ENDPOINT_AQUI")
AZURE_KEY = os.getenv("AZURE_LANGUAGE_KEY", "COLE_A_CHAVE_AQUI")

# O GCP exige o caminho do arquivo JSON nas variáveis de ambiente do SO
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/caminho/para/chave.json"

try:
    gcp_client = language_v2.LanguageServiceClient()
    azure_client = TextAnalyticsClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_KEY)
    )
except Exception as e:
    print(f"⚠️ Configure as credenciais no ambiente antes de executar. Detalhe: {e}")

# ==========================================
# 2. DATASET E PREPARAÇÃO (ABLACÃO DE CONTEXTO)
# ==========================================
print("Carregando dataset 'ramondomiingos/ptbr-irony-idioms-regionalism'...")
dataset = load_dataset("ramondomiingos/ptbr-irony-idioms-regionalism", split="train")
df = dataset.to_pandas()

def extrair_frase_sem_contexto(texto):
    """Extrai apenas a frase entre aspas, removendo a cena."""
    match = re.search(r"['\"](.*?)['\"]", str(texto))
    return match.group(1) if match else texto

df['Frase_Isolada'] = df['Texto de Entrada'].apply(extrair_frase_sem_contexto)

# As chamadas às APIs e o pipeline de métricas foram processados e salvos em CSV.
# Os resultados finais encontram-se na pasta /dados/
