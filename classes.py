from typing import List

class Property:
    def __init__(self, id_property : str, type : str, direction=None):
        self.id_property = id_property
        self.type = type
        self.direction = direction

    def __repr__(self):
        return f"{self.id_property} ({self.type})"


class Instance:
    def __init__(self, id_interne : str, id_externe : str, classe : str, type_bloc : str, properties : List[Property]):
        self.id_interne = id_interne
        self.id_externe = id_externe
        self.classe = classe
        self.type_bloc = type_bloc
        self.properties = properties

    def __repr__(self):
        return f"{self.classe} (ID {self.id_externe})"


class Class:
    def __init__(self, classe : str, connected_classes : List[str], properties : List[Property]):
        self.classe = classe
        self.connected_classes = connected_classes
        self.properties = properties

    def __repr__(self):
        return self.classe