from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class PreprocessStage(ABC):
    @abstractmethod
    def process(self, document: BeautifulSoup): ...
