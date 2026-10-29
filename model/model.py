from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        # Creo le variabili così se si verifica un errore prima dell'assegnazione
        # di una connessione o un cursore rimangono None e il finally può funzionare.
        #Così posso chiudere correttamente tutto sia se tutto funziona sia se si generano delle eccezioni
        connection = None
        cursor = None
        # Stabilire la connessione con il database
        try:
            connection=get_connection()
            if connection is None:  #Comunico che la connessione non è riuscita
                return None

            cursor = connection.cursor(dictionary=True) #Creo un cursore
                                                        # che mi serve per muovermi all'interno della base di dati

            #Query SQL per recuperare gli strumenti del database
            query = "SELECT * FROM STRUMENTO"
            cursor.execute(query)

            #Leggere le righe restituite dal database e creare una lista con tutti gli strumenti
            strumenti = []  #lista in cui inserire gli strumenti letti dal database

            for riga in cursor:
                s=Strumento(riga['codice'], riga['tipo'], riga['marca'], riga['anno_acquisto'], riga['valore'], riga['disponibile'])
                strumenti.append(s)

            return strumenti

        except Exception as errore:
            print(f"Errore nel recupero dei dati: {errore}")
            return None

        finally:  #sia che le istruzioni funzionino, sia che si verifichi un errore
                  # bisogna chiudere il cursore e la connessione
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()


    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        connection = None
        cursor = None

        try:
            connection=get_connection()
            if connection is None:
                return None
            cursor = connection.cursor(dictionary=True)
            query = ("""SELECT *
                     FROM Strumento
                     WHERE tipo = %s""")

            cursor.execute(query, (tipo,)) #esegue la ricerca usando il tipo ricevuto

            strumenti = []

            for riga in cursor:
                s=Strumento(riga['codice'], riga['tipo'], riga['marca'], riga['anno_acquisto'], riga['valore'], riga['disponibile'])
                strumenti.append(s)
            return strumenti

        except Exception as errore:
            print(f'Errore nella ricerca degli strumenti: {errore}')
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()


