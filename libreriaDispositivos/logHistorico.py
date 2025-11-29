from abc import ABC, abstractmethod


class LogHistorico(ABC):


    @abstractmethod
    def guardaLog(self, fichero: str):
        pass