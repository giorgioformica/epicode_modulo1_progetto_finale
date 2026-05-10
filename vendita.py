class Vendita:
    def __init__(self, data, negozio, prodotto, quantita, prezzo_unitario):
        self.data = data
        self.negozio = negozio
        self.prodotto = prodotto
        self.quantita = int(quantita)
        self.prezzo_unitario = float(prezzo_unitario)

    def __str__(self):
        return (
            f"{self.data} - {self.negozio} - {self.prodotto} - "
            f"{self.quantita} pezzi - {self.prezzo_unitario:.2f} €"
        )

    def calcola_incasso(self):
        return round(self.quantita * self.prezzo_unitario, 2)