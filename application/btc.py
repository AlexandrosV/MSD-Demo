class BTC:
    """
    BTC is s representation of Bitcoin price in EUR & CZK at a given timestamp
    Haven't got the chance to use this class :)
    """

    def __init__(self, price_eur, price_czk, price_time):
        self.price_eur = price_eur
        self.price_czk = price_czk
        self.price_time = price_time

    def description(self):
        return f"{self.__class__.__name__} price was {self.price_eur} EUR / {self.price_czk} CZK at {self.price_time}"

# Module methods 
def average_price(data):
    # Better validation is needed here
    total_eur = 0
    total_czk = 0
    count_eur = 0
    count_czk = 0
    if data:
        for item in data:
            if item['eur']:
                count_eur = count_eur + 1
                total_eur = total_eur + int(item['eur'])
            if item['czk']:
                count_czk = count_czk + 1
                total_czk = total_czk + int(item['czk'])
        total_eur = total_eur / count_eur
        total_czk = total_czk / count_czk
        
    return total_eur, total_czk