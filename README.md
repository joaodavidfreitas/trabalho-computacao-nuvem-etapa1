# Avaliação de APIs de PLN em Nuvem: Contexto, Ironia e Regionalismos ☁️🧠

Este repositório contém os códigos, datasets e apresentação da avaliação de desempenho das APIs comerciais de Processamento de Linguagem Natural (Google Cloud Natural Language e Microsoft Azure AI Language) no reconhecimento de ironias e regionalismos no Português Brasileiro.

**Instituição:** Universidade de Fortaleza (Unifor)  
**Disciplina:** Ambientes em nuvem para ciência de dados e inteligência artificial (Doutorado)  
**Autores:** João David de Freitas Cesário, Sérgio Maia Raulino, Ana Paula Silva de Araujo  

## 🎯 Objetivo e Metodologia
Comparar a acurácia de modelos baseados em léxico (GCP e Azure) utilizando um **Teste de Ablação** de contexto. 
1. **Com Contexto:** Texto integral contendo descrições de cenário (ex: `[Cliente irritado] 'Parabéns pela velocidade'`).
2. **Sem Contexto:** Fala extraída isoladamente via Regex (ex: `'Parabéns pela velocidade'`).

**Dataset:** `ramondomiingos/ptbr-irony-idioms-regionalism` (Hugging Face - 90 frases).

## 📊 Resultados e Conclusão
| Cenário | Google Cloud (GCP) | Microsoft Azure |
| :--- | :---: | :---: |
| **Com Contexto** | 37.78% | 27.78% |
| **Sem Contexto** | 30.00% | 23.33% |

Os resultados confirmaram uma alta taxa de Falsos Positivos em frases irônicas. Ferramentas de análise de sentimentos puramente baseadas na valência do léxico tendem a falhar drasticamente ao processar figuras de linguagem e pragmática cultural, dependendo severamente de marcações de contexto explícitas.

## 📂 Estrutura do Repositório
- `/dados`: Bases CSV geradas contendo os outputs brutos de ambas as nuvens.
- `/imagens`: Gráficos gerados da matriz de confusão e comparação de acurácia.
- `/src/analise_nuvem.py`: Código sanitizado do pipeline utilizado.
- `apresentacao_pln_nuvem_unifor.pdf`: Slides finais da pesquisa.

*(Nota de segurança: O código foi higienizado. Nenhuma chave de API ou credencial está exposta no repositório).*
