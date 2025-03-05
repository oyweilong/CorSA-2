from callbacks import Callbacks
import cv2
import glob
from keybindings import Keybindings
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from results_table import ResultsTable
from SAM import predictor
from set_colour import ColourGui
import set_scale
import tkinter as tk

class WelcomeGuiFuncs(tk.Tk, Callbacks):

    def open_next(self):
        self.reset_mask()
        currentindex = self.imgdir.index(self.current_file)
        if currentindex < (len(self.imgdir)-1):
            currentindex += 1
            self.current_file = self.imgdir[currentindex]
            self.filename = os.path.basename(self.current_file)
            self.open_img()
        else:
            tk.messagebox.showinfo("Error",  "End of directory")

    def open_previous(self):
        self.reset_mask()
        currentindex = self.imgdir.index(self.current_file)
        if currentindex > 0:
            currentindex -= 1
            self.current_file = self.imgdir[currentindex]
            self.filename = os.path.basename(self.current_file)
            self.open_img()
        else:
            tk.messagebox.showinfo("Error",  "End of directory")

    def open_img(self):
        plt.close(self.fig)
        self.fig,self.ax = plt.subplots()
        self.image = plt.imread(self.current_file)
        if self.current_file.endswith(".png"):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)
        self.ax.imshow(self.image)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.fig.canvas.manager.set_window_title(os.path.basename(self.current_file))
        predictor.set_image(self.image)
        self.mngr=plt.get_current_fig_manager()
        self.mngr.window.geometry("+600+250")
        self.zoom_factory(self.ax)
        self.onclick_func()
        self.keypress_id = plt.connect('key_press_event', self.keypress)
        self.update_scales()
        plt.show()
    
    def directory_setup(self, filedir):
        self.current_file = filedir
        self.filename = os.path.basename(filedir)
        file_dir = os.path.dirname(filedir)
        self.currentdir_label.config(text='Current File: '+ self.filename)
        imgdir = sorted(glob.glob(file_dir +  "/*.jpg") + glob.glob(file_dir +  "/*.jpeg") + glob.glob(file_dir +  "/*.png"))
        self.imgdir = [w.replace('\\','/') for w in imgdir]
        self.dir_image_no.config(text='Total no. of images: '+ str(len(imgdir)))
        self.update_idletasks()

        self.image = plt.imread(filedir)
        if filedir.endswith(".png"):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)
        self.fig,self.ax = plt.subplots()
        self.ax.imshow(self.image)
        self.fig.canvas.manager.set_window_title(self.filename)
        self.mngr=plt.get_current_fig_manager()
        self.mngr.window.geometry("+600+250")
        predictor.set_image(self.image)
        self.zoom_factory(self.ax)
        self.cid = plt.connect('button_press_event', self.multi_click)
        self.keypress_id = plt.connect('key_press_event', self.keypress)
        # self.onclick_func()
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        plt.show()

    def onclick_func(self):
        plt.disconnect(self.cid)
        if self.maskoption.get() == 'single':
            self.cid = plt.connect('button_press_event', self.single_click)
            self.keypress_id = plt.connect('key_press_event', self.keypress)
        if self.maskoption.get() == 'multi':
            self.cid = plt.connect('button_press_event', self.multi_click)
            self.keypress_id = plt.connect('key_press_event', self.keypress)

    def browse_dir(self):
        filedir= tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("JPEG Files","*.jpg"),("PNG Files", "*.png"),("All Files","*.*")))
        self.directory_setup(filedir)

    def enter_dir(self):
        filedir = self.dir_var.get()
        self.directory_setup(filedir)

    def setscale_btn(self):
        self.clear_mask()
        
        try:
            self.setscale
        except:
            self.setscale = set_scale.ScaleGui(self.ax, self.refresh_scale, self.onclick_func, self.cid)
            self.setscale.scaleoption.set(self.scale_state.get())
            self.setscale.update_idletasks()
        else:
            self.setscale.linedist=-1
            self.setscale.linecoords=[]
            self.setscale.ax = self.ax
            self.setscale.scaleoption.set(self.scale_state.get())
            self.setscale.update_idletasks()
            self.setscale.deiconify()
            plt.disconnect(self.cid)
            self.cid = plt.connect('button_press_event', self.setscale.drawline)
            self.setscale.scalepress_id = plt.connect('key_press_event', self.setscale.scalepress)
            self.setscale.grab_set()
    
    def setcolour_btn(self):
        self.clear_mask()
        try:
            self.setcolour
        except:
            plt.disconnect(self.keypress_id)
            self.setcolour = ColourGui(self.image, self.ax, self.refresh_colour, self.onclick_func, self.cid)
            self.setcolour.set_state.set(self.colourscaletype.get())

        else:
            self.setcolour.set_state.set(self.colourscaletype.get())
            self.setcolour.deiconify()
            for txt in self.ax.texts:
                txt.set_visible(True)
            for patch in self.ax.patches:
                patch.set_visible(True)
            plt.show()
            plt.disconnect(self.cid)
            plt.disconnect(self.keypress_id)
            self.setcolour.set_callbacks()
            self.setcolour.colpress_id = plt.connect('key_press_event', self.setcolour.colpress)
            self.setcolour.grab_set()
    
    def update_scales(self):
        try:
            self.setcolour
        except:
            pass
        else:
            self.setcolour.image = self.image
            self.setcolour.ax = self.ax
        try:
            self.setscale
        except:
            pass
        else:
            self.setscale.ax = self.ax
    
    def show_keybindings(self):
        if self.keybindings is None:
            self.keybindings = Keybindings()

        elif self.keybindings .winfo_viewable() == 0:
            self.keybindings .deiconify()

    def show_results_table(self):
        if self.results_table is None:
                self.results_table = ResultsTable()

        elif self.results_table.winfo_viewable() == 0:
                self.results_table.deiconify()

    def set_mask(self):
       self.onclick_func()
       self.reset_mask()
       
    def clear_mask(self):
        if self.current_mask != None:
            self.current_mask.remove()
            self.current_mask = None
            plt.show()

    def reset_mask(self):
        self.clear_mask()
        self.input_point = np.full((1,2),0)
        self.input_label = np.empty((1,1))
        
    def refresh_colour(self, **kwargs):
        for scaletype, scale in kwargs.items():
            if scaletype == 'loc':
                self.colourscale = scale
                
            elif scaletype == 'glob':
                self.colourcoords = scale
       

    def refresh_scale(self, **kwargs):
        for scaletype, scale in kwargs.items():
            if scaletype == 'loc':
                self.localscale = scale

                if self.localscale == None:
                    self.local_lab.config(text='Local Scale: '+ str(self.localscale))
                    self.update_idletasks()
                else:
                    self.local_lab.config(text='Local Scale: '+ str(round(self.localscale,2)) + ' pixels/cm')
                    self.update_idletasks()

            elif scaletype == 'glob':
                self.globalscale = scale

                if self.globalscale == None:
                    self.global_lab.config(text='Global Scale: '+ str(self.globalscale))
                    self.update_idletasks()
                else:
                    self.global_lab.config(text='Global Scale: '+ str(round(self.globalscale,2)) + ' pixels/cm')
                    self.update_idletasks()

    def measure(self):
        try:
            self.current_mask
        except:
            tk.messagebox.showinfo("Error",  "Mask is not drawn")
        else:
            if self.results_table is None:
                self.results_table = ResultsTable()
            
            if self.results_table.winfo_viewable() == 0:
                self.results_table.deiconify()

            name = self.filename[:-4]
            area = ""
            gmd = ""
            colour = ""
            update_dict = {"Photo ID": name}
            self.find_biggest_mask()

            if self.check_area.get()==1:
                if self.scale_state.get() == 'local' and self.localscale == None:
                    tk.messagebox.showinfo("Error",  "Scale is not set")
                elif self.scale_state.get() == 'global' and self.globalscale == None:
                    tk.messagebox.showinfo("Error",  "Scale is not set")
                self.get_area(update_dict)

            if self.check_GMD.get()==1:
                if self.scale_state.get() == 'local' and self.localscale == None:
                    tk.messagebox.showinfo("Error",  "Scale is not set")
                elif self.scale_state.get() == 'global' and self.globalscale == None:
                    tk.messagebox.showinfo("Error",  "Scale is not set")
                self.get_gmd(update_dict)
            
            if self.check_colour.get()==1:
                if self.colourscaletype.get() == 'local' and self.colourscale == None:
                    tk.messagebox.showinfo("Error",  "Colour reference is not set")
                elif self.colourscaletype.get() == 'global' and self.colourcoords == None:
                    tk.messagebox.showinfo("Error",  "Colour reference is not set")
                self.get_colour(update_dict)

            self.results_table.add_row(**update_dict)
            self.results_table.table.redraw()

    def get_area(self, update_dict):
        if self.scale_state.get() == 'local':
                area = self.selected_contour_area/(self.localscale* self.localscale)
                update_dict["Area (cm2)"]= round(area, 4)

        else:
            self.scale_state.get() == 'global'
            area = self.selected_contour_area/(self.globalscale* self.globalscale)
            update_dict["Area (cm2)"]= round(area, 4) 
    
    def get_gmd(self, update_dict):
        rect = cv2.minAreaRect(self.selected_contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        box_firstpoint=[box[0]]
        box = np.concatenate((box, box_firstpoint))
        x, y = zip(*box)
        plt.plot(x, y, color = 'r')
        center, size, angle = rect

        if self.scale_state.get() == 'local':
                width = size[0]/self.localscale
                height = size[1]/self.localscale

        elif self.scale_state.get() == 'global':
                width = size[0]/self.globalscale
                height = size[1]/self.globalscale

        gmd = math.sqrt(width * height)
        update_dict["GMD (cm)"]= round(gmd, 4)
        if width > height:
            update_dict["Max length (cm)"]= round(width, 4)
            update_dict["Width (cm)"] = round(height, 4)
        else:
            update_dict["Max length (cm)"]= round(height, 4)
            update_dict["Width (cm)"] = round(width, 4)

        plt.show()

    def get_colour(self, update_dict):
        average_colour = cv2.mean(self.image, mask = self.mask_reshaped)[::-1]
        average_colour = (int(average_colour[1]), int(average_colour[2]), int(average_colour[3]))
        average_colour = np.uint8([[average_colour]])
        average_hsv = cv2.cvtColor(average_colour, cv2.COLOR_BGR2HSV).flatten()
        h,s,v = average_hsv
        
        if self.colourscaletype.get() == 'local':
            lowest_diff = 99999
            closest_colour = None
            for i, k  in enumerate(self.colourscale):
                if type(self.colourscale[k][0]) == str:
                    pass
                else:
                    difference = abs(int(h) - self.colourscale[k][0]) + abs(int(s) - self.colourscale[k][1])+ abs(int(v) - self.colourscale[k][2])
                    if difference < lowest_diff:
                        lowest_diff = difference
                        closest_colour = k
            update_dict["Colour"] = closest_colour
        
        elif self.colourscaletype.get() == 'global':
            for i, k in enumerate(self.colourcoords):
                if type(self.colourcoords[k][0]) == str:
                    pass
                else:
                    x = self.colourcoords[k][0]
                    y = self.colourcoords[k][1]
                    
                    input_point = np.array([[x, y]])
                    input_label = np.array([1])
                    mask, _, _ = predictor.predict(
                    point_coords=input_point,
                    point_labels=input_label,
                    multimask_output=False,
                    )
                    height, width = self.mask.shape[-2:]
                    mask_reshaped = np.reshape(mask, (height,width))
                    mask_reshaped =mask_reshaped.astype(np.uint8)
                    average_colour = cv2.mean(self.image, mask = mask_reshaped)[::-1]
                    average_colour = (int(average_colour[1]), int(average_colour[2]), int(average_colour[3]))
                    average_colour = np.uint8([[average_colour]])
                    average_hsv = cv2.cvtColor(average_colour, cv2.COLOR_BGR2HSV).flatten()

                    a,b,c = average_hsv
                    self.global_dict[k][0] = a
                    self.global_dict[k][1] = b
                    self.global_dict[k][2] = c
                

            lowest_diff = 99999
            closest_colour = None
            for i, k  in enumerate(self.global_dict):

                difference = abs(int(h) - int(self.global_dict[k][0])) + abs(int(s) - int(self.global_dict[k][1]))+ abs(int(v) - int(self.global_dict[k][2]))
                if difference < lowest_diff:
                    lowest_diff = difference
                    closest_colour = k
            update_dict["Colour"] = closest_colour
         
            
            
    
    def find_biggest_mask(self):
        h, w = self.mask.shape[-2:]
        mask_reshaped = np.reshape(self.mask, (h,w))
        self.mask_reshaped =mask_reshaped.astype(np.uint8)
        contours,_= cv2.findContours(self.mask_reshaped, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        self.selected_contour = None
        self.selected_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.selected_contour_area:
                self.selected_contour = contour
                self.selected_contour_area = area
        
   
