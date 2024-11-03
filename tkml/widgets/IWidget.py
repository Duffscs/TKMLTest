import tkinter as tk
import xml.etree.ElementTree as ET
if 1 == 0:
    from tkml.TkmlPageAssembler import TkmlPageAssembler
class IWidget:
    name = None
    def __init__(self, pageAssember : 'TkmlPageAssembler'):
        self.pageAssembler = pageAssember
    
    def validate(self, element : ET.Element):
        if self.name is None:
            raise NotImplementedError("La propriété name doit être définie dans la classe dérivée {}.".format(self.__class__.__name__))
        return element.tag.lower() == self.name
    
    def create(self, element : ET.Element, parent : tk.Tk):
        raise NotImplementedError("La méthode create doit être implémentée dans la classe dérivée.")