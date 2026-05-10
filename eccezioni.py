class CSVFileNotFoundError(Exception):
    """Errore sollevato quando il file CSV non viene trovato."""
    pass

class CSVColumnsError(Exception):
    """Errore sollevato quando il CSV non contiene le colonne richieste."""
    pass

class EmptyDataFrameError(Exception):
    """Errore sollevato quando il DataFrame è vuoto."""
    pass

class InvalidDataError(Exception):
    """Errore sollevato quando i dati non sono validi."""
    pass

class MissingCategoryError(Exception):
    """Errore sollevato quando un prodotto non ha una categoria associata."""
    pass