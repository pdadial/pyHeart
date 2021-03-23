
import numpy as np
import matplotlib.animation as animation

class RealtimePlotWindow:

    def __init__(self, title: str, fig, ax, txt=False):
        """

        Initialises an instance of animation class for realtime plotting.
        Parameters
        ----------
        title : subplot title
        fig : instance of figure
        ax : array of axes
        txt : boolean value to indicate text plotting
    
        """
        self.ax = ax
        if not txt:
            self.ax.set_title(f"{title}")
            # that's our plotbuffer
            self.plotbuffer = np.zeros(100)
            # create an empty line
            self.line, = self.ax.plot(self.plotbuffer[-100:])
            # axis
            self.ax.set_ylim(0, 1)
        
        else:
            # that's our text buffer
            self.txtbuffer = 0
            self.ax.text(0.5, 0.6, "Heartrate [in BPM]", verticalalignment='bottom', horizontalalignment='center', transform=self.ax.transAxes, color='r', fontsize=15)
            self.line = self.ax.text(0.5, 0.4, f"{self.txtbuffer}", verticalalignment='bottom', horizontalalignment='center', transform=self.ax.transAxes, color='r', fontsize=15)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []

        # start the animation
        self.ani = animation.FuncAnimation(fig, self.update, fargs=[txt], interval=100)


    def update(self, data, txt):
        """

        Updates the plot.
        Parameters
        ----------
        data : frame number
        txt : boolean value to indicate text plotting
        
        Returns
        -------
        line : tuple of plot objects
        
        """
        if not txt:
            # add new data to the buffer
            self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
            # only keep the 500 newest ones and discard the old ones
            self.plotbuffer = self.plotbuffer[-100:]
            self.ringbuffer = []
            # set the new 500 points of channel 9
            self.line.set_ydata(self.plotbuffer[-100:])
            self.ax.set_ylim(min(self.plotbuffer)-1, max(self.plotbuffer)+5)
            
        else:
            self.txtbuffer = self.ringbuffer[-1:]
            self.ringbuffer = []
            self.line.set_text(f"{self.txtbuffer}")
        
        return self.line,


    def addData(self, v):
        """

        Appends data to the ringbuffer.
        Parameters
        ----------
        v : new value
        txt : boolean value to indicate text plotting
    
        """
        self.ringbuffer.append(v)