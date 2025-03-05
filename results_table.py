import tkinter as tk
from tkintertable import TableCanvas


data = {'0': {'Photo ID': ''}
       }

class ResultsTable(tk.Toplevel):

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry('800x500+200+100')
        self.title('Results Table')
        f = tk.Frame(self)
        f.pack(fill='both',expand=1)
    
        self.table = TableCanvas(f, data = data, rowheaderwidth=100,showkeynamesinheader=True, read_only = False)
        self.table.show()
        self.table.model.columnNames.clear()
        self.protocol("WM_DELETE_WINDOW", self.wm_withdraw)

        # column_headers= ['Photo ID', 'Area','Colour','GMD','Length','Width', 'Remarks']
        self.column_headers = ['Photo ID', 'Remarks']
        for header in range(len(self.column_headers)):
            self.table.addColumn(self.column_headers[header])
        self.row_counter=1

    def add_columns(self, area, GMD, colour):
        pass

    def add_row(self, **kwargs):
        self.table.addRow(self.row_counter, **kwargs)
        self.row_counter+=1 
    

if __name__ == '__main__':
    ResultsTable().mainloop()

