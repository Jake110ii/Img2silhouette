import matplotlib.pyplot as plt
import numpy as np
import matplotlib.widgets as wg
import matplotlib.gridspec as gridspec
import matplotlib
matplotlib.use('WebAgg')

import utils.NearestNeighbor as near


class Img2silhouette():
    def __init__(self, gs):
        self.ax0 = plt.subplot(gs[0, :])
        self.ax1 = plt.subplot(gs[1, 0])
        self.ax2 = plt.subplot(gs[1, 1])
        self.ax3 = plt.subplot(gs[1, 2])
        self.ln, = self.ax0.plot([],[],'bo')
        self.cur, = self.ax0.plot([],[],'ro')
        self.x = []
        self.y = []
        self._xlim = [-500, 4000]
        self._ylim = [-400, 2000]
        self.ax0.set_xlim(-500, 4000)
        self.ax0.set_ylim(-400, 2000)
        self.line_pre = None
        self.btn2mode = Btn2mode(self)
        self.mode_switch = "onclick"
        self.first_flg = "first"
        self.btn_flg = "off"

        # motion
        self.gco = None
        self.xdata = None
        self.ydata = None
        self.ind = None
        self.mo_id = None
        self.onc_id = None
        self.onp_id = None
   
    def onclick(self, event):
        if not (0 < event.xdata <=1 and 0 < event.ydata <= 1):
            x = event.xdata
            y = event.ydata
            self.x.append(x)
            self.y.append(y)

            self.cur.set_data(x, y)
            self.ln.set_data(self.x, self.y)
            plt.draw()

    def btn_silhouette_click(self, event):
        if self.line_pre is not None:
            self.line_pre.remove()

        # nearest sort
        self.x, self.y = near.nearest_sort(self.x, self.y)
        self.line_pre, = self.ax0.plot(self.x + [self.x[0]], self.y + [self.y[0]], "o-", picker=15)
        self.cur.set_data(self.x[0], self.y[0])
        self.ln.set_data(self.x, self.y)
        plt.draw()
        
    # motion
    def motion(self, event):
        if self.gco is None:
            return
        x = event.xdata
        y = event.ydata
        if x == None or y == None:
            return

        # 始点と終点は一緒に動かす
        if self.ind == 0:
            self.xdata[-1] = x
            self.ydata[-1] = y
            self.x[-1] = x
            self.y[-1] = y

        self.xdata[self.ind] = x
        self.ydata[self.ind] = y
        self.x[self.ind] = x
        self.y[self.ind] = y
        self.gco.set_data(self.xdata,self.ydata)
        
        # point move
        self.cur.set_data(self.x[0], self.y[0])
        self.ln.set_data(self.x, self.y)
 
        plt.draw()

    def onpick(self, event):
        self.gco = event.artist
        self.xdata = self.gco.get_xdata()
        self.ydata = self.gco.get_ydata()
        self.ind = event.ind[0]

    def release(self, event):
        self.gco = None

    def setup_callbacks(self):
        if self.mode_switch == "onclick":
            print('### onclick event start ###')
            fig.canvas.mpl_disconnect(self.onp_id)
            self.onc_id = fig.canvas.mpl_connect('button_press_event', self.onclick)

            if self.mo_id is not None:
                fig.canvas.mpl_disconnect(self.mo_id)

        # motion
        if self.mode_switch == "motion":
            print('### motion event start ###')
            fig.canvas.mpl_disconnect(self.onc_id)
            self.onp_id = fig.canvas.mpl_connect('pick_event', self.onpick)
            self.mo_id = fig.canvas.mpl_connect('motion_notify_event', self.motion)
            fig.canvas.mpl_connect('button_release_event', self.release)

        if self.first_flg == 'first':
            self.btn2mode.setup_callbacks()
            self.first_flg = 'not first'
            self.ax0.set_title('mode = {}'.format(self.mode_switch))
            plt.draw()

class Btn2mode:
    def __init__(self, img2silhouette):
        self.img2silhouette = img2silhouette
        self.btn_silh = wg.Button(img2silhouette.ax1, 'silhouette', color='#ffffff', hovercolor='#38b48b')
        self.btn_clear = wg.Button(img2silhouette.ax2, 'clear', color='#ffffff', hovercolor='#38b48b')
        self.btn_switch_mode = wg.Button(img2silhouette.ax3, 'switch mode', color='#ffffff', hovercolor='#38b48b')
        
    def btn_silhouette_click(self, event):
        self.img2silhouette.btn_silhouette_click(event)

    def btn_clear_click(self, event):
        # Clear all points
        self.img2silhouette.x.clear()
        self.img2silhouette.y.clear()
        self.img2silhouette.ln.set_data([], [])
        self.img2silhouette.cur.set_data([], [])
        if self.img2silhouette.line_pre is not None:
            self.img2silhouette.line_pre.remove()
            self.img2silhouette.line_pre = None
        plt.draw()

    def btn_switch_mode_click(self, event):
        if self.img2silhouette.mode_switch == "onclick":
            self.img2silhouette.mode_switch = "motion"
            print("Switched to motion mode")
            self.img2silhouette.setup_callbacks()
            self.btn_flg = "on"
        elif self.img2silhouette.mode_switch == "motion":
            self.img2silhouette.mode_switch = "onclick"
            print("Switched to onclick mode")
            self.img2silhouette.setup_callbacks()
            self.img2silhouette.btn_flg = "on"

        self.img2silhouette.ax0.set_title('mode = {}'.format(self.img2silhouette.mode_switch))
        plt.draw()

    def setup_callbacks(self):
        self.btn_silh.on_clicked(self.btn_silhouette_click)
        self.btn_clear.on_clicked(self.btn_clear_click)
        self.btn_switch_mode.on_clicked(self.btn_switch_mode_click)


fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(2, 3, height_ratios=(8, 1))
img2silhouette = Img2silhouette(gs)
img2silhouette.setup_callbacks()
plt.show()
