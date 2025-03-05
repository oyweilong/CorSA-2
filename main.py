import numpy as np
import tkinter as tk
from welcome_gui_funcs import WelcomeGuiFuncs

class WelcomeGui(WelcomeGuiFuncs):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Welcome to CorSA 2! v1.0.0")
        gui_width = 550
        gui_height = 500
        screenw = self.winfo_screenwidth()
        screenh = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (gui_width, gui_height, 0, (screenh/2)-(gui_height/2)))
        # self.fig_geom = str('+'+'')
        self.make_topmost()
        
        self.dir_var = tk.StringVar(self)
        self.maskoption = tk.StringVar(self, value = 'multi')
        self.current_mask = None
        self.input_point = np.full((1,2),0)
        
        self.colourscale = None
        self.colourcoords = None
        self.colourscaletype = tk.StringVar(self, value = 'global')
        self.global_dict = dict.fromkeys(range(1,7))
        for i in range(1,7):
            self.global_dict[i] = [0,0,0]

        self.scale_state = tk.StringVar(self, value = 'global')
        self.localscale= None
        self.globalscale= None
        self.filename = None
        self.results_table = None
        self.keybindings = None
        self.imgdir= []

        inputdir_label=tk.Frame(self)
        dir_label = tk.Label(inputdir_label, text = '1) Select first image to process: ', font=('calibre',10, 'bold'))
        dir_entry = tk.Entry(inputdir_label,textvariable = self.dir_var, font=('calibre',10,'normal'))
        enter_btn = tk.Button(inputdir_label,text = 'Enter', command = self.enter_dir)
        browse_btn = tk.Button(inputdir_label,text = 'Browse', command = self.browse_dir)   

        dir_label.pack(side='left', padx=10, pady=10)
        dir_entry.pack(side='left', padx=10, pady=10, expand = True)
        enter_btn.pack(side='left', padx=10, pady=10)
        browse_btn.pack(side='left', padx=10, pady=10)

        currentdir_label=tk.Frame(self)
        self.currentdir_label = tk.Label(currentdir_label, text = 'Current File: ', font=('calibre',10))
        self.dir_image_no = tk.Label(currentdir_label, text = 'Total no. of images: ', font=('calibre',10))

        self.currentdir_label.pack(side='left', padx=10, pady=10, expand = True, anchor = 'w')
        self.dir_image_no.pack(side='left', padx=10, pady=10)

        setscale_label=tk.Frame(self)
        scale_label = tk.Label(setscale_label, text = '4) Select scale (Surface area /GMD): ', font=('calibre',10, 'bold'))
        self.local_lab = tk.Radiobutton(setscale_label, text = 'Local Scale: None', variable = self.scale_state, value = 'local', 
                                        indicator = 0, bg = 'light blue', font=('calibre',10))
        self.global_lab = tk.Radiobutton(setscale_label, text = 'Global Scale: None', variable = self.scale_state, value = 'global',
                                         indicator = 0, bg = 'light blue', font=('calibre',10))
        setscale_btn = tk.Button(setscale_label,text = 'Scale Settings', command = self.setscale_btn)
        
        scale_label.pack(side='top')
        self.local_lab.pack(side='left', padx=10, pady=10)
        self.global_lab.pack(side='left', padx=10, pady=10)
        setscale_btn.pack(side='left', padx=10, pady=10)

        coloursettingsrow = tk.Frame(self)
        colour_label = tk.Label(coloursettingsrow, text = '5) Select colour reference (Colour score): ', font=('calibre',10, 'bold'))
        colour_local = tk.Radiobutton(coloursettingsrow,text = 'Local', variable = self.colourscaletype, value = 'local')
        colour_global = tk.Radiobutton(coloursettingsrow,text = 'Global', variable = self.colourscaletype, value = 'global')
        coloursettings_btn = tk.Button(coloursettingsrow,text = 'Colour Settings', command = self.setcolour_btn)

        colour_label.pack(side='top')
        colour_local.pack(side='left', padx = 10, pady = 10)
        colour_global.pack(side='left', padx = 10, pady = 10)
        coloursettings_btn.pack(side='right', padx=10, pady=10)

        checkboxes = tk.Frame(self)
        self.check_area = tk.IntVar(value = 1)
        self.check_GMD = tk.IntVar()
        self.check_colour = tk.IntVar()
        measurements_label = tk.Label(checkboxes, text = '2) Select which measurements to take: ', font=('calibre',10, 'bold'))
        area_btn = tk.Checkbutton(checkboxes, text = 'Surface Area (cm2)', variable = self.check_area, onvalue=1, offvalue=0, height = 2, width=20)
        gmd_btn = tk.Checkbutton(checkboxes, text = 'GMD (cm)', variable = self.check_GMD, onvalue=1, offvalue=0, height = 2, width=10)
        colour_btn = tk.Checkbutton(checkboxes, text = 'Colour Score', variable = self.check_colour, onvalue=1, offvalue=0, height = 2, width=10)
        measurements_label.pack(side='top')
        area_btn.pack(side='left', padx=5, pady=10)
        gmd_btn.pack(side='left', padx=5, pady=10)
        colour_btn.pack(side='left', padx=5, pady=10)

        masksettings = tk.Frame(self)
        mask_label = tk.Label(masksettings, text = '3) Select which mask to use: ', font=('calibre',10, 'bold'))
        single_click_btn = tk.Radiobutton(masksettings,text = 'Single Click', variable = self.maskoption, value = 'single', command = self.set_mask)
        multiple_click_btn = tk.Radiobutton(masksettings,text = 'Multi Click', variable = self.maskoption, value = 'multi', command = self.set_mask)
        reset_mask_btn = tk.Button(masksettings, text = 'Reset Mask', command = self.reset_mask)

        mask_label.pack(side='top')
        single_click_btn.pack(side='left', padx = 10, pady = 10)
        multiple_click_btn.pack(side='left', padx = 10, pady = 10)
        reset_mask_btn.pack(side='left', padx = 10, pady = 10)

        measure_row=tk.Frame(self)
        measure_label = tk.Label(measure_row, text = '6) Measure! ', font=('calibre',10, 'bold'))
        prev_btn = tk.Button(measure_row, text = 'Previous image', command = self.open_previous)
        measure_btn = tk.Button(measure_row,text = 'Measure', command = self.measure, bg = 'light green', width = 40)
        next_btn = tk.Button(measure_row, text = 'Next image', command = self.open_next)

        measure_label.pack(side='top')
        next_btn.pack(side='right', padx=10, pady=10)
        measure_btn.pack(side='right', padx=10, pady=10 )
        prev_btn.pack(side='right', padx=10, pady=10)
        
        misc_row=tk.Frame(self)
        controls_btn = tk.Button(misc_row,text = 'Key Bindings', command = self.show_keybindings)
        resultstable_btn = tk.Button(misc_row,text = 'Results Table', command = self.show_results_table)
        
        controls_btn.pack(side='left', padx=10, pady=10)
        resultstable_btn.pack(side='left', padx=10, pady=10)

        # test_btn = tk.Button(self,text = 'Test', command = self.test, bg = 'light green')

        inputdir_label.pack()
        currentdir_label.pack()
        checkboxes.pack()
        masksettings.pack()
        setscale_label.pack()
        coloursettingsrow.pack()
        measure_row.pack()
        misc_row.pack()
    
        # test_btn.pack(padx=10, pady=10)


if __name__ == '__main__':
    WelcomeGui().mainloop()
    
    
    