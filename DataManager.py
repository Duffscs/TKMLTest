import json
from typing import List
from classes import Class, Property, Instance

class DataManager():
    def __init__(self):
        self.instances : List[Instance] = []
        self.classes : List[Property] = []

    def load_data(self):
        with open("class.json", "r") as f:
            classes_data = json.load(f)
            for root in classes_data:
                self.classes.append(Class(
                    classe=root["classe"], 
                    connected_classes=root["connected_classes"], 
                    properties=[Property(**prop) for prop in root["properties"]])
                )

        with open("instances.json", "r") as f:
            instances_data = json.load(f)
            for instance in instances_data:
                self.instances.append(Instance(
                    id_interne=instance["id_interne"], 
                    id_externe=instance["id_externe"], 
                    classe=instance["classe"], 
                    type_bloc=instance["type_bloc"], 
                    properties=[Property(**prop) for prop in instance["properties"]]
                ))
    
    def save_data(self):
        with open("class.json", "w") as f:
            json.dump([root.__dict__ for root in self.classes], f, default=lambda o: o.__dict__, indent=4)
