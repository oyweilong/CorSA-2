import tkinter as tk

class Keybindings(tk.Tk):
    def __init__(self):    
        tk.Tk.__init__(self)
        self.title("Key Bindings")
        self.geometry("300x400")
        self.protocol("WM_DELETE_WINDOW", self.wm_withdraw)

        kb_text = 'Previous image = "q"\nMeasure = "w"\nNext image = "e"\nZoom in = "mouse wheel up\nZoom out = "mouse wheel down"' 
        
        keybindings_label = tk.Label(self, text = 'In Image Window', font=('calibre',10, 'bold'))
        keybindings_text = tk.Label(self, text = kb_text, font=('calibre',10 ))
       
        keybindings_label.pack(side='top', padx=10, pady=1)
        keybindings_text.pack(side='top', padx=5, pady=2)
        
        single_text = 'Single mask:\nRegions to include = "left click"'
        multi_text = 'Multi mask:\nRegions to include = "left click"\nRegions to exclude = "right click"\nReset mask = "r"'

        maskbindings_label = tk.Label(self, text = 'Mask Bindings', font=('calibre',10, 'bold'))
        singlemask_text = tk.Label(self, text = single_text, font=('calibre',10 ))
        multimask_text = tk.Label(self, text = multi_text, font=('calibre',10 ))

        maskbindings_label.pack(side='top', padx=10, pady=1)
        singlemask_text.pack(side='top', padx=5, pady=2)
        multimask_text.pack(side='top', padx=5, pady=2)


        scale_text = 'Set scale = "space bar"'

        scale_bindings_label = tk.Label(self, text = 'Scale Settings', font=('calibre',10, 'bold'))
        scale_bindings_text = tk.Label(self, text = scale_text, font=('calibre',10 ))

        scale_bindings_label.pack(side='top', padx=10, pady=1)
        scale_bindings_text.pack(side='top', padx=5, pady=2)

        colour_text = 'Colour score 1 to 6 = "1" to "6"\n Set colour = "space bar"'

        colour_bindings_label = tk.Label(self, text = 'Colour Settings', font=('calibre',10, 'bold'))
        colour_bindings_text = tk.Label(self, text = colour_text, font=('calibre',10 ))

        colour_bindings_label.pack(side='top', padx=10, pady=1)
        colour_bindings_text.pack(side='top', padx=5, pady=2)

if __name__ == '__main__':
    Keybindings().mainloop()
    
    
