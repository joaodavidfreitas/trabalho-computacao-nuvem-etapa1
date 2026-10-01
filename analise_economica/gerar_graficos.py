import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "precos.csv")
OUT = os.path.join(BASE, "graficos")

os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(CSV)

# ============================================================
# PLN
# ============================================================

pln = df[
    (df["categoria"] == "PLN") &
    (df["preco"].notna())
].copy()

custos = []

for _, row in pln.iterrows():
    preco = float(row["preco"])
    unidade = row["unidade"]

    if "100 caracteres" in unidade:
        custo = 1_000_000 / 100 * preco
    elif "1000 caracteres" in unidade:
        custo = 1_000_000 / 1000 * preco
    else:
        continue

    custos.append({
        "Provedor": row["provedor"],
        "Custo": custo
    })

if custos:
    plot_df = pd.DataFrame(custos)

    plt.figure(figsize=(8, 5))
    plt.bar(
        plot_df["Provedor"],
        plot_df["Custo"]
    )
    plt.title(
        "PLN — Custo para 1 milhão de caracteres"
    )
    plt.ylabel("Custo (USD)")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUT,
            "custo_pln_1_milhao_caracteres.png"
        ),
        dpi=200
    )

    plt.close()


# ============================================================
# VISÃO
# ============================================================

visao = df[
    (df["categoria"] == "Visão") &
    (df["preco"].notna())
].copy()

custos = []

for _, row in visao.iterrows():
    preco = float(row["preco"])

    custos.append({
        "Provedor": row["provedor"],
        "Custo": 10_000 * preco
    })

if custos:
    plot_df = pd.DataFrame(custos)

    plt.figure(figsize=(8, 5))
    plt.bar(
        plot_df["Provedor"],
        plot_df["Custo"]
    )
    plt.title(
        "Visão — Custo para 10 mil imagens"
    )
    plt.ylabel("Custo (USD)")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUT,
            "custo_visao_10_mil_imagens.png"
        ),
        dpi=200
    )

    plt.close()


# ============================================================
# DOCUMENTOS
# ============================================================

docs = df[
    (df["categoria"] == "Documentos") &
    (df["preco"].notna())
].copy()

custos = []

aws = docs[
    docs["provedor"] == "AWS"
]["preco"].astype(float).sum()

gcp = docs[
    docs["provedor"] == "GCP"
]["preco"].astype(float).sum()

if aws > 0:
    custos.append({
        "Provedor": "AWS",
        "Custo": 10_000 * aws
    })

if gcp > 0:
    custos.append({
        "Provedor": "GCP",
        "Custo": 10_000 * gcp
    })

if custos:
    plot_df = pd.DataFrame(custos)

    plt.figure(figsize=(8, 5))
    plt.bar(
        plot_df["Provedor"],
        plot_df["Custo"]
    )
    plt.title(
        "Documentos — Custo para 10 mil páginas"
    )
    plt.ylabel("Custo (USD)")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUT,
            "custo_documentos_10_mil_paginas.png"
        ),
        dpi=200
    )

    plt.close()


print("Gráficos gerados com sucesso.")
print("Diretório:", OUT)
