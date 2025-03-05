from callbacks import Callbacks
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

class ColourGui(tk.Toplevel, Callbacks):

    def __init__(self, image, ax, refreshcolourfunc, onclickfunc, cid):
        tk.Toplevel.__init__(self)
        
        self.title("Set Colour")
        self.geometry("500x400")
        self.image = image
        self.ax = ax
        self.refresh = refreshcolourfunc
        self.onclick_func = onclickfunc
        self.cid = cid
        self.colour_state = tk.IntVar(self, value = 6)
        self.set_state = tk.StringVar(self, value = 'global')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.set_callbacks()
        self.colpress_id = plt.connect('key_press_event', self.colpress)
        self.grab_set()
        self.hsv_dict = dict.fromkeys(range(1,7))
        for i in range(1,7):
            self.hsv_dict[i] = ['H: ','S: ','V: ']

        self.coords_dict = dict.fromkeys(range(1,7))
        for i in range(1,7):
            self.coords_dict[i] = ['X','Y', 'circle', 'letter']
        
        colour_scale=tk.Frame(self)
        self.score_6 = tk.Radiobutton(colour_scale, text = 'Colour 6', variable = self.colour_state, value = 6, 
                                        indicator = 0, bg = '#3C2A00', font=('calibre',10, 'bold'))
        self.score_5 = tk.Radiobutton(colour_scale, text = 'Colour 5', variable = self.colour_state, value = 5,
                                            indicator = 0, bg = '#5F4916', font=('calibre',10, 'bold'))
        self.score_4 = tk.Radiobutton(colour_scale, text = 'Colour 4', variable = self.colour_state, value = 4,
                                            indicator = 0, bg = '#967323', font=('calibre',10, 'bold'))
        self.score_3 = tk.Radiobutton(colour_scale, text = 'Colour 3', variable = self.colour_state, value = 3,
                                            indicator = 0, bg = '#BE9A46', font=('calibre',10, 'bold'))
        self.score_2 = tk.Radiobutton(colour_scale, text = 'Colour 2', variable = self.colour_state, value = 2,
                                            indicator = 0, bg = '#DCB55A', font=('calibre',10, 'bold'))
        self.score_1 = tk.Radiobutton(colour_scale, text = 'Colour 1', variable = self.colour_state, value = 1,
                                            indicator = 0, bg = '#ECC363', font=('calibre',10, 'bold'))
        self.set_colour_btn = tk.Button(colour_scale,text = 'Set Colour', command = self.set_colour)
        
        self.score_6.pack(side='left', pady=10, expand = True, fill = 'both')
        self.score_5.pack(side='left', pady=10, expand = True, fill = 'both')
        self.score_4.pack(side='left', pady=10, expand = True, fill = 'both')
        self.score_3.pack(side='left', pady=10, expand = True, fill = 'both')
        self.score_2.pack(side='left', pady=10, expand = True, fill = 'both')
        self.score_1.pack(side='left', pady=10, expand = True, fill = 'both')
        self.set_colour_btn.pack(side='left', padx=10, expand = True, fill = 'both')

        global_btn_frame = tk.Frame(self)
        self.global_btn = tk.Radiobutton(global_btn_frame, text = 'Set Global Reference Coordinates', font=('calibre',10, 'bold'), 
                                         variable = self.set_state, indicator = 0, bg = 'lightblue', value = 'global', command = self.set_callbacks)
        self.global_btn.pack(side='left', padx=10, expand = True, fill = 'both')


        global_coords=tk.Frame(self)
        self.coords_6 = tk.Label(global_coords, text = 'X: \nY: ')
        self.coords_5 = tk.Label(global_coords, text = 'X: \nY: ')
        self.coords_4= tk.Label(global_coords, text = 'X: \nY: ')
        self.coords_3 = tk.Label(global_coords, text = 'X: \nY: ')
        self.coords_2 = tk.Label(global_coords, text = 'X: \nY: ')
        self.coords_1 = tk.Label(global_coords, text = 'X: \nY: ')
        
        self.coords_6.pack(side='left', padx=10, expand = True, fill = 'both')
        self.coords_5.pack(side='left', padx=10, expand = True, fill = 'both')
        self.coords_4.pack(side='left', padx=10, expand = True, fill = 'both')
        self.coords_3.pack(side='left', padx=10, expand = True, fill = 'both')
        self.coords_2.pack(side='left', padx=10, expand = True, fill = 'both')
        self.coords_1.pack(side='left', padx=10, expand = True, fill = 'both')


        local_btn_frame = tk.Frame(self)
        self.local_btn = tk.Radiobutton(local_btn_frame, text = 'Set Local HSV', font=('calibre',10, 'bold'), 
                                        variable = self.set_state, indicator = 0, bg = 'lightblue', value = 'local', command = self.set_callbacks)
        self.local_btn.pack(side='left', padx=10, expand = True, fill = 'both')

        local_h=tk.Frame(self)
        self.hsv6 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        self.hsv5 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        self.hsv4 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        self.hsv3 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        self.hsv2 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        self.hsv1 = tk.Label(local_h, text = 'H: \nS: \nV: ')
        
        self.hsv6.pack(side='left', padx=10, expand = True, fill = 'both')
        self.hsv5.pack(side='left', padx=10, expand = True, fill = 'both')
        self.hsv4.pack(side='left', padx=10, expand = True, fill = 'both')
        self.hsv3.pack(side='left', padx=10, expand = True, fill = 'both')
        self.hsv2.pack(side='left', padx=10, expand = True, fill = 'both')
        self.hsv1.pack(side='left', padx=10, expand = True, fill = 'both')
        
        reset_btn_frame = tk.Frame(self)
        self.reset_btn = tk.Button(reset_btn_frame,text = 'Reset All Local/Global References', command = self.reset_colour)
        self.reset_btn.pack(side='left', padx=10, expand = True, fill = 'both')

        colour_scale.pack(pady=20, fill = 'x')
        global_btn_frame.pack(pady = 20, fill = 'x')
        global_coords.pack(fill = 'x')
        local_btn_frame.pack(pady = 20, fill = 'x')
        local_h.pack(fill = 'x')
        reset_btn_frame.pack(pady = 20, fill = 'x')

    def set_colour(self):
        if self.set_state.get() == "local":
            self.set_local_hsv()
        elif self.set_state.get() == "global":
             self.set_global_coords()

    def set_callbacks(self):
        self.clear_mask()
        plt.disconnect(self.cid)
        if self.set_state.get() == "local":
            self.cid = plt.connect('button_press_event', self.single_click)

        elif self.set_state.get() == "global":
            self.cid = plt.connect('button_press_event', self.draw_coord_positions)

    def set_local_hsv(self):
        plt.disconnect(self.cid)
        self.cid = plt.connect('button_press_event', self.single_click)
        colour_selected = self.colour_state.get()
        average_hsv = self.get_colour()
        h,s,v = average_hsv
        self.hsv_dict[colour_selected][0] = h
        self.hsv_dict[colour_selected][1] = s
        self.hsv_dict[colour_selected][2] = v
        self.refresh(loc= self.hsv_dict)
        
        if colour_selected == 6:
            self.hsv6.config(text= f'H: {h}\nS: {s}\nV: {v}')
        elif colour_selected == 5:
            self.hsv5.config(text= f'H: {h}\nS: {s}\nV: {v}')
        elif colour_selected == 4:
            self.hsv4.config(text= f'H: {h}\nS: {s}\nV: {v}')
        elif colour_selected == 3:
            self.hsv3.config(text= f'H: {h}\nS: {s}\nV: {v}')
        elif colour_selected == 2:
            self.hsv2.config(text= f'H: {h}\nS: {s}\nV: {v}')
        elif colour_selected == 1:
            self.hsv1.config(text= f'H: {h}\nS: {s}\nV: {v}')
    
        self.update_idletasks()

        
    def set_global_coords(self):
        plt.disconnect(self.cid)
        self.cid = plt.connect('button_press_event', self.draw_coord_positions)
        colour_selected = self.colour_state.get()
        self.refresh(glob = self.coords_dict)

        if colour_selected == 6:
            self.coords_6.config(text = f'X: {self.coords_dict[6][0]}\nY: {self.coords_dict[6][1]}')
        if colour_selected == 5:
            self.coords_5.config(text = f'X: {self.coords_dict[5][0]}\nY: {self.coords_dict[5][1]}')
        if colour_selected == 4:
            self.coords_4.config(text = f'X: {self.coords_dict[4][0]}\nY: {self.coords_dict[4][1]}')
        if colour_selected == 3:
            self.coords_3.config(text = f'X: {self.coords_dict[3][0]}\nY: {self.coords_dict[3][1]}')
        if colour_selected == 2:
            self.coords_2.config(text = f'X: {self.coords_dict[2][0]}\nY: {self.coords_dict[2][1]}')
        if colour_selected == 1:
            self.coords_1.config(text = f'X: {self.coords_dict[1][0]}\nY: {self.coords_dict[1][1]}')   

        self.update_idletasks()

    def get_colour(self):
            h, w = self.mask.shape[-2:]
            mask_reshaped = np.reshape(self.mask, (h,w))
            self.mask_reshaped =mask_reshaped.astype(np.uint8)
            average_colour = cv2.mean(self.image, mask = self.mask_reshaped)[::-1]
            average_colour = (int(average_colour[1]), int(average_colour[2]), int(average_colour[3]))
            average_colour = np.uint8([[average_colour]])
            average_hsv = cv2.cvtColor(average_colour, cv2.COLOR_BGR2HSV).flatten()
            return average_hsv

    def reset_mask(self):
        self.clear_mask()

    def show_mask(self,mask, ax, random_color=False):
        self.mask = mask
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30/255, 144/255, 255/255, 0.6])
            h, w = mask.shape[-2:]
            mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
            self.current_mask = ax.imshow(mask_image)
            plt.show()   

    def clear_mask(self):
        try:
            self.current_mask
        except:
            pass
        else:
            if self.current_mask != None:
                self.current_mask.remove()
                self.current_mask = None
                plt.show() 

    def reset_colour(self):
        if self.set_state.get() == 'local':
            self.clear_mask()
            self.hsv_dict = dict.fromkeys(range(1,7))
            for i in range(1,7):
                self.hsv_dict[i] = ['H: ','S: ','V: ']

            self.hsv6.config(text= 'H: \nS: \nV: ')
            self.hsv5.config(text= 'H: \nS: \nV: ')
            self.hsv4.config(text= 'H: \nS: \nV: ')
            self.hsv3.config(text= 'H: \nS: \nV: ')
            self.hsv2.config(text= 'H: \nS: \nV: ')
            self.hsv1.config(text= 'H: \nS: \nV: ')
            self.update_idletasks()

        elif self.set_state.get() == 'global':
            for i, k in enumerate(self.coords_dict):
                if isinstance(self.coords_dict[k][2], str) == False:
                    self.coords_dict[k][2].remove()
                    self.coords_dict[k][3].remove()
            plt.show()
            
            self.coords_dict = dict.fromkeys(range(1,7))
            for i in range(1,7):
                self.coords_dict[i] = ['X','Y', 'circle', 'letter']
            
            self.coords_6.config(text = 'X: \nY: ')
            self.coords_5.config(text = 'X: \nY: ')
            self.coords_4.config(text = 'X: \nY: ')
            self.coords_3.config(text = 'X: \nY: ')
            self.coords_2.config(text = 'X: \nY: ')
            self.coords_1.config(text = 'X: \nY: ')
            self.update_idletasks()
        
    def close(self):
        self.clear_mask()
        for txt in self.ax.texts:
            txt.set_visible(False)
        for patch in self.ax.patches:
            patch.set_visible(False)
        plt.show()
        plt.disconnect(self.cid)
        plt.disconnect(self.colpress_id)
        self.onclick_func()
        self.grab_release()
        self.wm_withdraw()
    
    def colpress(self, event):
        if event.key == '1':
            self.colour_state.set(1)
            self.update_idletasks()
        if event.key == '2':
            self.colour_state.set(2)
            self.update_idletasks()
        if event.key == '3':
            self.colour_state.set(3)
            self.update_idletasks()
        if event.key == '4':
            self.colour_state.set(4)
            self.update_idletasks()
        if event.key == '5':
            self.colour_state.set(5)
            self.update_idletasks()
        if event.key == '6':
            self.colour_state.set(6)
            self.update_idletasks()
        if event.key == ' ':
            self.set_colour()
        if event.key == 'r':
            self.reset_colour()
        if event.key == 't':
            self.close()


