from tkml import TkmlPage, ArrayVar
import tkinter as tk
from enum import Enum

class DialogResult(Enum):
    OK = 1
    CANCEL = 2
    CLOSE = 3

class ComboDialog(TkmlPage):

    def __init__(self, items, title="Choix de l'option", text="Sélectionnez une option:", selected_index=0, **kwargs):
        super().__init__(**kwargs)
        self.cbValues = ArrayVar(value=items)
        self.selected_index = tk.IntVar(value=selected_index)
        self.selected_item = tk.StringVar(value=items[selected_index])
        self.title = tk.StringVar(value=title)
        self.text = tk.StringVar(value=text)
        self.onCancel = lambda: None
        self.onOk = lambda: None
        self.result = DialogResult.CLOSE
        #center the window taking into account the window size
        self.root.geometry(f"+{self.root.winfo_screenwidth()//2-150}+{self.root.winfo_screenheight()//2-50}")

    def get_tkml(self):
        return """
        <Window title="{{ title }}" width="300" height="100" layout="grid">
            <Label text="{{ text }}" row="0" column="0" />
            <ComboBox state="readonly" values="{Binding cbValues}" selected_item="{Binding selected_item}" 
                selected_index="{Binding selected_index}" row="0" column="1" />
            <Button text="Annuler" row="1" column="0" command="_Cancel" />
            <Button text="Ok" row="1" column="1" command="_Ok" />
        </Window>
        """
    
    def _Cancel(self):
        self.result = DialogResult.CANCEL
        self.selected_index.set(-1)
        self.onCancel()
        self.close()

    def _Ok(self):
        self.result = DialogResult.OK
        self.onOk()
        self.close()