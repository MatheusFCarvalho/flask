from typing import Dict, List, Union
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

class RepositorierOfAll:
    def __init__(self, database) -> None:
        self.database = database
        self.collectionsDict: Dict[str, Collection] = {}
        self.collectionsArr: List[Collection] = []

    def adicionarCollection(self, keyOfCollection: str) -> Collection:
        collection = self.database[keyOfCollection]
        self.collectionsDict[keyOfCollection] = collection
        self.collectionsArr.append(collection)
        return collection

    def adicionarDocumento(self, documento: dict, guiaCollection: Union[str, int]) -> InsertOneResult:
        """
        Adiciona um documento a uma coleção especificada.

        Args:
            documento (dict): O documento a ser inserido na coleção.
            guiaCollection (Union[str, int]): A chave da coleção ou o índice da lista de coleções onde o documento será inserido.

        Raises:
            KeyError: Se a chave da coleção não for encontrada no dicionário de coleções.
            IndexError: Se o índice da coleção não for encontrado na lista de coleções.
        """
        if isinstance(guiaCollection, str):
            self.collectionsDict[guiaCollection].insert_one(documento)
        elif isinstance(guiaCollection, int):
            self.collectionsArr[guiaCollection].insert_one(documento)

    def encontrarDocumento(self, filtro: dict, guiaCollection: Union[str, int]):
        """
        Encontra documentos em uma coleção especificada com base em um filtro.
        """
        if isinstance(guiaCollection, str):
            return self.collectionsDict[guiaCollection].find_one(filtro)
        elif isinstance(guiaCollection, int):
            return self.collectionsArr[guiaCollection].find_one(filtro)

    def atualizarDocumento(self, filtro: dict, atualizacao: dict, guiaCollection: Union[str, int]) -> UpdateResult:
        """
        Atualiza um documento em uma coleção especificada.
        """
        if isinstance(guiaCollection, str):
            return self.collectionsDict[guiaCollection].update_one(filtro, atualizacao)
        elif isinstance(guiaCollection, int):
            return self.collectionsArr[guiaCollection].update_one(filtro, atualizacao)

    def deletarDocumento(self, filtro: dict, guiaCollection: Union[str, int]) -> DeleteResult:
        """
        Deleta um documento de uma coleção especificada.
        """
        if isinstance(guiaCollection, str):
            return self.collectionsDict[guiaCollection].delete_one(filtro)
        elif isinstance(guiaCollection, int):
            return self.collectionsArr[guiaCollection].delete_one(filtro)

    def adicionarDocumentos(self, documentos: List[dict], guiaCollection: Union[str, int]):
        """
        Adiciona múltiplos documentos a uma coleção especificada.
        """
        if isinstance(guiaCollection, str):
            return self.collectionsDict[guiaCollection].insert_many(documentos)
        elif isinstance(guiaCollection, int):
            return self.collectionsArr[guiaCollection].insert_many(documentos)

    def atualizarDocumentos(self, filtro: dict, atualizacao: dict, guiaCollection: Union[str, int]) -> UpdateResult:
        """
        Atualiza múltiplos documentos em uma coleção especificada.
        """
        if isinstance(guiaCollection, str):
            return self.collectionsDict[guiaCollection].update_many(filtro, atualizacao)
        elif isinstance(guiaCollection, int):
            return self.collectionsArr[guiaCollection].update_many(filtro, atualizacao)
