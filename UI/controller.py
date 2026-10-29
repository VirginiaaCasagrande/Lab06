import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler

    def handler_mostra_strumenti(self,e):
        strumenti=self._model.get_strumenti()  #il Controller chiama il metodo get_strumenti() del Model
        self._view.lista_strumenti.controls.clear()

        if strumenti is None:  #get_strumenti() può restituire anche None, quindi non una lista valida
            self._view.lista_strumenti.controls.append(ft.Text('Errore'))
        else:
            for strumento in strumenti:
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        self._view.update()

    def handler_cerca_strumenti(self, e):
        tipo=self._view.input_tipo_strumento.value  #recupero il valore inserito dall'utente
        strumenti=self._model.cerca_strumenti_per_tipo(tipo) #chiamo il metodo di cricerca degli strumenti del Model
        self._view.lista_strumenti_ricerca.controls.clear()

        if strumenti is None:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text('Errore'))
        elif strumenti == []:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text('Nessun strumento trovato'))
        else:
            for strumento in strumenti:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        self._view.update()


