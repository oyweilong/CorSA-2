from callbacks import Callbacks
import matplotlib.pyplot as plt
import tkinter as tk

class ScaleGui(tk.Toplevel, Callbacks):

    def __init__(self, ax, refresh, onclick_func, cid):
        tk.Toplevel.__init__(self)
        self.ax=ax
        self.refresh=refresh
        self.title("Set Scale")
        self.geometry("500x150")
        self.make_topmost()
        self.linedist=-1
        self.linecoords=[]
        self.protocol("WM_DELETE_WINDOW", self.close)
        plt.disconnect(cid)
        self.cid = plt.connect('button_press_event', self.drawline)
        self.scalepress_id = plt.connect('key_press_event', self.scalepress)
        self.onclick_func = onclick_func
        self.grab_set()
     
        self.scaleoption = tk.StringVar(self,name = "scaleoption", value = 'global')
        scale_var = tk.StringVar(self, name = "scale")

        firstrow=tk.Frame(self)
        scale_label = tk.Label(firstrow, text = 'Known Distance:', font=('calibre',10, 'bold'))
        scale_entry = tk.Entry(firstrow,textvariable = scale_var, font=('calibre',10,'normal'))
        set_btn = tk.Button(firstrow,text = 'Set Distance', command = self.set_scale)
        res_btn = tk.Button(firstrow,text = 'Reset All', command = self.reset_all)

        scale_label.pack(side='left', padx=10, pady=10)
        scale_entry.pack(side='left', padx=10, pady=10, expand=True)
        set_btn.pack(side='left', padx = 10, pady = 10)
        res_btn.pack(side='left', padx = 10, pady = 10)

        secondrow=tk.Frame(self)
        self.local_display = tk.Label(secondrow, text = 'Current Local Scale: None')
        set_local_btn = tk.Radiobutton(secondrow,text = 'Set Local Scale', variable = self.scaleoption, value = 'local', command =self.reset_lines)
        res_local_btn = tk.Button(secondrow,text = 'Reset', command = self.reset_local)

        self.local_display.pack(side='left', padx=10, pady=10, expand=True)
        set_local_btn.pack(side='left', padx = 10, pady = 10)
        res_local_btn.pack(side='left', padx = 10, pady = 10)

        thirdrow=tk.Frame(self)
        self.global_display = tk.Label(thirdrow, text = 'Current Global Scale: None')
        set_global_btn = tk.Radiobutton(thirdrow,text = 'Set Global Scale', variable = self.scaleoption, value = 'global', command = self.reset_lines)
        res_global_btn = tk.Button(thirdrow,text = 'Reset', command = self.reset_global)

        self.global_display.pack(side='left', padx=10, pady=10, expand=True)
        set_global_btn.pack(side='left', padx = 10, pady = 10)
        res_global_btn.pack(side='left', padx = 10, pady = 10)

        firstrow.pack()
        secondrow.pack()
        thirdrow.pack()
        
    def set_scale(self):
        scale=self.getvar(name = "scale")
        if self.linedist < 0:
            self.error_msg1()
        else:
            try:
                float(scale)
            except ValueError:
                self.error_msg2()
            else:
                finalscale = self.linedist/float(scale)
                self.make_topmost()
                scale_state = str(self.getvar(name = "scaleoption"))

                if scale_state == "local":
                    self.local_display.config(text='Current Local Scale: '+ str(round(finalscale,2))+ ' pixels/cm')
                    self.update_idletasks()
                    self.refresh(loc=finalscale)
                
                elif scale_state == "global":
                    self.global_display.config(text='Current Global Scale: '+ str(round(finalscale,2))+ ' pixels/cm')
                    self.update_idletasks()
                    self.refresh(glob=finalscale) 
    
            
    def error_msg1(self):
        tk.messagebox.showinfo("Error",  "Line is not drawn")
        

    def error_msg2(self):
        tk.messagebox.showinfo("Error",  "Invalid scale input")
        
    
    def reset_all(self):
        for line in self.ax.get_lines():
                line.remove()
        for patch in self.ax.patches:
                patch.remove()
        plt.show()
        self.linecoords.clear()
        self.linedist=-1
        self.make_topmost()
        self.local_display.config(text='Current Local Scale: None')
        self.global_display.config(text='Current Global Scale: None')
        self.refresh(loc = None, glob = None)
        self.update_idletasks()
    
    def reset_local(self):
        for line in self.ax.get_lines():
                line.remove()
        for patch in self.ax.patches:
                patch.remove()
        plt.show()
        self.linecoords.clear()
        self.linedist=-1
        self.make_topmost()
        self.local_display.config(text='Current Local Scale: None')
        self.refresh(loc = None)
        self.update_idletasks()

    def reset_global(self):
        for line in self.ax.get_lines():
                line.remove()
        for patch in self.ax.patches:
                patch.remove()
        plt.show()
        self.linecoords.clear()
        self.linedist=-1
        self.make_topmost()
        self.global_display.config(text='Current Global Scale: None')
        self.refresh(glob = None)
        self.update_idletasks()

    def reset_lines(self):
        for line in self.ax.get_lines():
                line.remove()
        for patch in self.ax.patches:
                patch.remove()
        plt.show()
        self.linecoords.clear()
        self.linedist=-1

    def close(self):
        for line in self.ax.get_lines():
                line.remove()
        for patch in self.ax.patches:
                patch.remove()
        plt.show()
        plt.disconnect(self.cid)
        self.onclick_func()
        self.grab_release()
        self.wm_withdraw()
    
    def scalepress(self, event):
        if event.key == ' ':
            self.set_scale()
        if event.key == 'r':
            self.reset_all()
        if event.key == 't':
            self.close()
        
        
