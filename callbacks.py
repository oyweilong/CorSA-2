import math
from matplotlib.backend_bases import MouseButton
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np
from SAM import predictor

class Callbacks():
    def single_click(self, event):
        if event.button is MouseButton.LEFT:
            self.reset_mask()
            input_point = np.array([[event.xdata, event.ydata]])
            input_label = np.array([1])
            mask, _, _ = predictor.predict(
                point_coords=input_point,
                point_labels=input_label,
                multimask_output=False,
            )
            self.show_mask(mask, plt.gca())

            
    def multi_click(self, event):
        if event.button is MouseButton.LEFT:
            self.clear_mask()
            if np.sum(self.input_point[0]) == 0:
                self.input_point[0] = [event.xdata, event.ydata]
                self.input_label = np.array([1])
            else:
                self.input_point = np.append(self.input_point, [[event.xdata, event.ydata]], axis = 0)
                self.input_label = np.append(self.input_label, 1)
            
            mask, _, _ = predictor.predict(
                point_coords=self.input_point,
                point_labels=self.input_label,
                multimask_output=False,
            )
            self.show_mask(mask, plt.gca())
        
        if event.button is MouseButton.RIGHT:
            self.clear_mask()
            if np.sum(self.input_point[0]) == 0:
                self.input_point[0] = [event.xdata, event.ydata]
                self.input_label = np.array([0])
            else:
                self.input_point = np.append(self.input_point, [[event.xdata, event.ydata]], axis = 0)
                self.input_label = np.append(self.input_label, 0)
            
            mask, _, _ = predictor.predict(
                point_coords=self.input_point,
                point_labels=self.input_label,
                multimask_output=False,
            )
            self.show_mask(mask, plt.gca())

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
            
    def drawline(self, event):
        if event.button is MouseButton.LEFT:
            
            x , y = int(event.xdata), int(event.ydata)
            self.linecoords.append((x, y))
            if len(self.linecoords) > 2:
                for line in self.ax.get_lines():
                    line.remove()
                for patch in self.ax.patches:
                    patch.remove()
                self.linecoords.pop(0)
                self.linecoords.pop(0)

            circle = plt.Circle((int(x),int(y)),5,color='black')
            self.ax.add_patch(circle)
            plt.show()

            if len(self.linecoords) == 2:
                x1 = (self.linecoords[0][0], self.linecoords[1][0])
                y1 = (self.linecoords[0][1], self.linecoords[1][1])
                line = lines.Line2D(x1,y1, color = "black", lw=3, axes =self.ax)
                self.ax.add_line(line)
                linedist = math.dist(self.linecoords[0],self.linecoords[1])
                self.linedist = linedist   

    def draw_coord_positions(self, event):
         if event.button is MouseButton.LEFT:
            colour_selected = self.colour_state.get()
            if self.coords_dict[colour_selected][3] != 'letter':
                self.coords_dict[colour_selected][2].remove()
                self.coords_dict[colour_selected][3].remove()
                self.coords_dict[colour_selected][2] = 'circle'
                self.coords_dict[colour_selected][3] = 'letter'

            x , y = int(event.xdata), int(event.ydata)
            self.coords_dict[colour_selected][2] = plt.Circle((int(x),int(y)),5,color='red')
            self.ax.add_patch(self.coords_dict[colour_selected][2])
            self.coords_dict[colour_selected][3] = plt.text(x, y+10, str(colour_selected), fontsize=20)
            self.coords_dict[colour_selected][0] = x
            self.coords_dict[colour_selected][1] = y
            plt.show()
            
         
    def set_callbacks(self):
        self.clear_mask()
        plt.disconnect(self.cid)
        # self.colpress_id = plt.connect('key_press_event', self.setcolour.colpress)
        if self.scale_state.get() == "local":
            self.cid = plt.connect('button_press_event', self.single_click)
 
        elif self.scale_state.get() == "global":
            self.cid = plt.connect('button_press_event', self.draw_coord_positions)
 

    def zoom_factory(self, ax , base_scale = 2.):
        def zoom_fun(event):
            # get the current x and y limits
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1/base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                # print event.button
            # set new limits
            ax.set_xlim([xdata - cur_xrange*scale_factor,
                        xdata + cur_xrange*scale_factor])
            ax.set_ylim([ydata - cur_yrange*scale_factor,
                        ydata + cur_yrange*scale_factor])
            plt.draw() # force re-draw
            
        fig = ax.get_figure() # get the figure of interest
        # attach the call back
        fig.canvas.mpl_connect('scroll_event',zoom_fun)

        #return the function
        return zoom_fun

    def keypress(self, event):
        if event.key == '1':
            self.setscale_btn()
        if event.key == '2':
            self.setcolour_btn()    
        if event.key == 'q':
            self.open_previous()
        if event.key == 'w':
            self.measure()
        if event.key == 'e':
            self.open_next()
        if event.key == 'r':
            self.reset_mask()
        
    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
