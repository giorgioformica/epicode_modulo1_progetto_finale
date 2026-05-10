import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from eccezioni import (
    CSVColumnsError,
    EmptyDataFrameError,
    InvalidDataError,
    MissingCategoryError
)

class AnalizzatoreVendite:
    def __init__(self, dataframe):
        self.df = dataframe

    def valida_dataframe(self):
        if self.df.empty:
            raise EmptyDataFrameError(
                "Il DataFrame è vuoto. Impossibile eseguire l'analisi."
            )

        colonne_richieste = [
            "Data",
            "Negozio",
            "Prodotto",
            "Quantità",
            "Prezzo_unitario"
        ]

        colonne_mancanti = []

        for colonna in colonne_richieste:
            if colonna not in self.df.columns:
                colonne_mancanti.append(colonna)

        if len(colonne_mancanti) > 0:
            raise CSVColumnsError(
                f"Nel CSV mancano queste colonne obbligatorie: {colonne_mancanti}"
            )

        if (self.df["Quantità"] <= 0).any():
            raise InvalidDataError(
                "La colonna Quantità contiene valori minori o uguali a zero."
            )

        if (self.df["Prezzo_unitario"] <= 0).any():
            raise InvalidDataError(
                "La colonna Prezzo_unitario contiene valori minori o uguali a zero."
            )

    def mostra_info_base(self):
        
        print("PARTE 2 - IMPORTAZIONE CON PANDAS")

        print("\nPrime 5 righe:")
        print(self.df.head())

        print("\nNumero righe e colonne:")
        print(self.df.shape)

        print("\nInformazioni generali:")
        print(self.df.info())

    def aggiungi_colonna_incasso(self):
        self.df["Incasso"] = self.df["Quantità"] * self.df["Prezzo_unitario"]
        self.df["Incasso"] = self.df["Incasso"].round(2)

    def analisi_pandas(self):
        
        print("PARTE 3 - ELABORAZIONI CON PANDAS")

        incasso_totale = self.df["Incasso"].sum()

        incasso_medio_per_negozio = pd.pivot_table(
            self.df,
            values="Incasso",
            index="Negozio",
            aggfunc="mean"
        )

        top_3_prodotti_quantita = pd.pivot_table(
            self.df,
            values="Quantità",
            index="Prodotto",
            aggfunc="sum"
        ).sort_values(by="Quantità", ascending=False).head(3)

        incasso_medio_negozio_prodotto = pd.pivot_table(
            self.df,
            values="Incasso",
            index=["Negozio", "Prodotto"],
            aggfunc="mean"
        )

        print(f"\nIncasso totale della catena: {incasso_totale:.2f} €")

        print("\nIncasso medio per negozio:")
        print(incasso_medio_per_negozio)

        print("\nTop 3 prodotti più venduti per quantità totale:")
        print(top_3_prodotti_quantita)

        print("\nIncasso medio per Negozio e Prodotto:")
        print(incasso_medio_negozio_prodotto)

    def analisi_numpy(self):
        
        print("PARTE 4 - USO DI NUMPY")

        quantita = self.df["Quantità"].to_numpy(dtype=np.int32)

        media = np.mean(quantita)
        minimo = np.min(quantita)
        massimo = np.max(quantita)
        deviazione_standard = np.std(quantita)

        vendite_sopra_media = quantita[quantita > media]
        percentuale_sopra_media = len(vendite_sopra_media) / len(quantita) * 100

        print(f"\nMedia quantità: {media:.2f}")
        print(f"Quantità minima: {minimo}")
        print(f"Quantità massima: {massimo}")
        print(f"Deviazione standard: {deviazione_standard:.2f}")
        print(f"Percentuale vendite sopra la media: {percentuale_sopra_media:.2f}%")

        array_2d = self.df[["Quantità", "Prezzo_unitario"]].to_numpy(dtype=np.float32)

        incassi_numpy = array_2d[:, 0] * array_2d[:, 1]
        incassi_numpy = np.round(incassi_numpy, 2)

        incassi_dataframe = self.df["Incasso"].to_numpy(dtype=np.float32)
        incassi_dataframe = np.round(incassi_dataframe, 2)

        confronto = np.allclose(incassi_numpy, incassi_dataframe)

        print("\nPrime 5 righe array 2D Quantità + Prezzo_unitario:")
        print(array_2d[:5])

        print("\nPrimi 5 incassi calcolati con NumPy:")
        print(incassi_numpy[:5])

        print("\nPrimi 5 incassi del DataFrame:")
        print(incassi_dataframe[:5])

        print(f"\nI risultati NumPy coincidono con la colonna Incasso: {confronto}")

    def crea_grafici(self):
        
        print("PARTE 5 - VISUALIZZAZIONI CON MATPLOTLIB")

        self.grafico_incasso_per_negozio()
        self.grafico_torta_incassi_per_prodotto()
        self.grafico_linee_incassi_giornalieri()

    def grafico_incasso_per_negozio(self):
        incasso_per_negozio = pd.pivot_table(
            self.df,
            values="Incasso",
            index="Negozio",
            aggfunc="sum"
        )

        plt.figure(figsize=(10, 6))
        incasso_per_negozio["Incasso"].plot(kind="bar")
        plt.title("Incasso totale per negozio")
        plt.xlabel("Negozio")
        plt.ylabel("Incasso")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("incasso_per_negozio.png")
        plt.show()

    def grafico_torta_incassi_per_prodotto(self):
        incasso_per_prodotto = pd.pivot_table(
            self.df,
            values="Incasso",
            index="Prodotto",
            aggfunc="sum"
        )

        plt.figure(figsize=(8, 8))
        incasso_per_prodotto["Incasso"].plot(
            kind="pie",
            autopct="%1.1f%%"
        )
        plt.title("Percentuale di incassi per prodotto")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig("incasso_per_prodotto.png")
        plt.show()

    def grafico_linee_incassi_giornalieri(self):
        self.df["Data"] = pd.to_datetime(self.df["Data"])

        incasso_giornaliero = pd.pivot_table(
            self.df,
            values="Incasso",
            index="Data",
            aggfunc="sum"
        )

        plt.figure(figsize=(10, 6))
        incasso_giornaliero["Incasso"].plot(kind="line", marker="o")
        plt.title("Andamento giornaliero degli incassi totali")
        plt.xlabel("Data")
        plt.ylabel("Incasso")
        plt.tight_layout()
        plt.savefig("andamento_giornaliero_incassi.png")
        plt.show()

    def aggiungi_categoria(self):
        categorie_prodotti = {
            "Smartphone": "Informatica",
            "Laptop": "Informatica",
            "Tablet": "Informatica",
            "Monitor": "Informatica",

            "TV": "Elettrodomestici",

            "Console": "Gaming",

            "Cuffie": "Accessori",
            "Mouse": "Accessori",
            "Tastiera": "Accessori",
            "Smartwatch": "Accessori"
        }

        self.df["Categoria"] = self.df["Prodotto"].map(categorie_prodotti)

        prodotti_senza_categoria = self.df[
            self.df["Categoria"].isna()
        ]["Prodotto"].unique()

        if len(prodotti_senza_categoria) > 0:
            raise MissingCategoryError(
                f"Questi prodotti non hanno una categoria associata: {prodotti_senza_categoria}"
            )

    def analisi_avanzata(self):
        
        print("PARTE 6 - ANALISI AVANZATA")

        self.aggiungi_categoria()

        riepilogo_categoria = pd.pivot_table(
            self.df,
            values=["Incasso", "Quantità"],
            index="Categoria",
            aggfunc={
                "Incasso": "sum",
                "Quantità": "mean"
            }
        )

        riepilogo_categoria["Incasso"] = riepilogo_categoria["Incasso"].round(2)
        riepilogo_categoria["Quantità"] = riepilogo_categoria["Quantità"].round(2)

        print("\nIncasso totale e quantità media per categoria:")
        print(riepilogo_categoria)

    def top_n_prodotti(self, n):
        prodotti = pd.pivot_table(
            self.df,
            values="Incasso",
            index="Prodotto",
            aggfunc="sum"
        )

        prodotti = prodotti.sort_values(by="Incasso", ascending=False)

        return prodotti.head(n)

    def grafico_combinato_categoria(self):
        
        print("PARTE 7 - ESTENSIONI")

        riepilogo_categoria = pd.pivot_table(
            self.df,
            values=["Incasso", "Quantità"],
            index="Categoria",
            aggfunc={
                "Incasso": "mean",
                "Quantità": "mean"
            }
        )

        fig, ax1 = plt.subplots(figsize=(10, 6))

        riepilogo_categoria["Incasso"].plot(
            kind="bar",
            ax=ax1
        )

        ax1.set_xlabel("Categoria")
        ax1.set_ylabel("Incasso medio")
        ax1.set_title("Incasso medio e quantità media per categoria")

        ax2 = ax1.twinx()

        riepilogo_categoria["Quantità"].plot(
            kind="line",
            marker="o",
            ax=ax2
        )

        ax2.set_ylabel("Quantità media")

        plt.tight_layout()
        plt.savefig("incasso_quantita_categoria.png")
        plt.show()