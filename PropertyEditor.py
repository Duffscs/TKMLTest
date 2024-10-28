from tkml import TkmlPage

class PropertyEditor(TkmlPage):
    def __init__(self, parent, property):
        super().__init__(parent=parent)
        self.property = property

    def get_tkml(self):
        return """
        <Window title="Éditeur de Propriété" width="400" height="200" layout="grid" row_weights="1,0,0" col_weights="1,1">
            
        </Window>
        """
