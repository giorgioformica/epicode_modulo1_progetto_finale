import pandas as pd

from eccezioni import CSVFileNotFoundError, EmptyDataFrameError

class CSVManager:
    def __init__(self, percorso_file):
        self.percorso_file = percorso_file

    def leggi_csv(self):
        try:
            df = pd.read_csv(
                self.percorso_file,
                sep=";",
                decimal=","
            )
        except FileNotFoundError:
            raise CSVFileNotFoundError(
                f"Il file CSV non è stato trovato: {self.percorso_file}"
            )

        if df.empty:
            raise EmptyDataFrameError(
                "Il file CSV è vuoto. Impossibile proseguire."
            )

        return df

    def salva_csv(self, dataframe, percorso_output):
        if dataframe.empty:
            raise EmptyDataFrameError(
                "Impossibile salvare un DataFrame vuoto."
            )

        dataframe.to_csv(
            percorso_output,
            index=False,
            sep=";",
            decimal=","
        )

        print(f"File salvato: {percorso_output}")