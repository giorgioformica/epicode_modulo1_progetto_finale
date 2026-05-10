"""
Progetto finale
Analisi di Vendite in una Catena di Negozi

"""

from csv_manager import CSVManager
from analizzatore_vendite import AnalizzatoreVendite

from eccezioni import (
    CSVFileNotFoundError,
    CSVColumnsError,
    EmptyDataFrameError,
    InvalidDataError,
    MissingCategoryError
)

def main():
    
    input_file = input("Inserisci il nome o percorso del file CSV delle vendite: ")
    output_file = "vendite_analizzate.csv"
    
    try:
        csv_manager = CSVManager(input_file)

        df = csv_manager.leggi_csv()

        analizzatore = AnalizzatoreVendite(df)

        analizzatore.valida_dataframe()

        analizzatore.mostra_info_base()

        analizzatore.aggiungi_colonna_incasso()

        analizzatore.analisi_pandas()

        analizzatore.analisi_numpy()

        analizzatore.crea_grafici()

        analizzatore.analisi_avanzata()

        csv_manager.salva_csv(
            analizzatore.df,
            output_file
        )

        print("\nTop 3 prodotti per incasso totale:")
        print(analizzatore.top_n_prodotti(3))

        analizzatore.grafico_combinato_categoria()

    except CSVFileNotFoundError as errore:
        print(f"Errore file CSV: {errore}")

    except CSVColumnsError as errore:
        print(f"Errore colonne CSV: {errore}")

    except EmptyDataFrameError as errore:
        print(f"Errore DataFrame vuoto: {errore}")

    except InvalidDataError as errore:
        print(f"Errore dati non validi: {errore}")

    except MissingCategoryError as errore:
        print(f"Errore categoria mancante: {errore}")

    except Exception as errore:
        print(f"Errore imprevisto: {errore}")
    
if __name__ == "__main__":
    main()