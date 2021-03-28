"""
Sheetly

Author: P.Huft

A tool for learning to read sheet music. In its simplest form it involves 
memorizing the positions of notes as they appear on a bass or treble clef.  

In the most basic mode, a random note is placed on a staff, plotted in 
matplotlib, and the user is asked to input the letter corresponding to the 
note. The correct answer is shown if the user gets it incorrect, and then the
user may advance the quiz. The validity of each responses (correct, incorrect)
is stored in a file for analysis by the user. 
"""

# imports 
import time
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class Sheetly:

    VERSION = 1.0
    _LETTERS = ['A','B','C','D','E','F','G']
    _NUMBERS = [n for n in range(1,7)]
    
    _LINESPACE = 2 
    _STAFF_GAP = 10
    _CLEF_LINES = 5
    
    def __init__(self):
        self.notes = self._notes()

        # bass clef bounds
        self.bmin = 0
        self.bmax = (self._CLEF_LINES - 1)*self._LINESPACE

        # treble clef bounds
        self.tmin = self.bmax + 10
        self.tmax = self.tmin + (self._CLEF_LINES - 1)*self._LINESPACE

        # range of allowed treble and bass note vertical positions
        self.treb_range = self._treb_range()
        self.bass_range = self._bass_range()

        # related to state control
        self.running = True
        self.drawings = []
    
    def _treb_range(self):
        return [i+self.bmax+self._STAFF_GAP 
                   for i in range(-2*self._LINESPACE,7*self._LINESPACE)]
    
    def _bass_range(self):
        return list(range(-2*self._LINESPACE, int(7*self._LINESPACE)))
    
    def _notes(self):
        return [f"{a}{n}" for n in self._NUMBERS for a in self._LETTERS]

    # TODO: make these functions are not in terms of the linespace
    def treb_y(self,y):
        """
        return treble note associated with y value
        """
        return self._LETTERS[y % 7] + str((y-2)//7+2)
    
    def bass_y(self,y):
        """
        return bass note associated with y value
        """
        return self._LETTERS[y % 7 - 1] + str(y//7+3)

    def draw_staff(self, xbounds=[0,20],ybounds=[-3,17],axis=False):
        """
        returns the Figure and AxesSubplot associated with the staff plot

        Plot ranges from 0-10 in y and 0-10
        """

        fig, ax = plt.subplots()

        for i in np.arange(self.bmin,self.bmax+1,self._LINESPACE):
            ax.axhline(i,c='k')
            
        for i in np.arange(self.tmin,self.tmax+1,self._LINESPACE):
            ax.axhline(i,c='k')

        ax.set_aspect('equal')
        ax.set_ylim(np.array(ybounds)*self._LINESPACE)
        ax.set_xlim(np.array(xbounds)*self._LINESPACE)
        if not axis:
            ax.axis('off')

        return fig, ax

    # TODO: make elliptical like actual note symbol
    def draw_notes(self, yvals, ax, xvals=None, duration=None):
        """
        Draws a Circle patch note on the ax passed in

        Args:
            yvals: the list of vertical note position(s) to be plotted
            xvals: the list of x location(s) on the staff. defaults 
            to center of ax if not specified 
            duration: str, optional. determines the filling of the note
            drawn. options are 'whole','half','quarter', etc 
            TODO implement
        """

        if xvals == None:
            x1,x2 = ax.get_xlim()
            xspan = x2-x1
            xvals = [(x1+x2/2)]*len(yvals)
        
        for y, x in zip(yvals, xvals):
            patch = ax.add_patch(Circle((x,y),0.5*self._LINESPACE
                                ,color='k'))
            self.drawings.append(patch)
            
            ticks = None # no extra "ticks" to draw; note appears in the clef

            use_treb = False
            use_bass = False
            if y in self.bass_range and y in self.treb_range:
                if np.floor(rand.random()+0.5):
                    use_bass = True
                else:
                    use_treb = True
    
            # TODO: fix logic for when y is in both treble and bass ranges
            if y in self.bass_range or use_bass:
                if y < self.bmin-0.5*self._LINESPACE:
                    ticks = (self.bmin - y) // self._LINESPACE
                    tick_ylist = [self.bmin - (i+1)*self._LINESPACE for i in range(ticks)]
                elif y > self.bmax-0.5*self._LINESPACE:
                    ticks = (y - self.bmax) // self._LINESPACE
                    tick_ylist = [self.bmax + (i+1)*self._LINESPACE for i in range(ticks)]
                if ticks:
                    for tick_y in tick_ylist:
                        line = ax.axhline(tick_y,
                                   xmin=(x-.75*self._LINESPACE)/xspan, 
                                   xmax=(x+.75*self._LINESPACE)/xspan, 
                                   c='k')
                        self.drawings.append(line)
                
            if y in self.treb_range or use_treb:
                if y < self.tmin-0.5*self._LINESPACE:
                    ticks = (self.tmin - y) // self._LINESPACE
                    tick_ylist = [self.tmin - (i+1)*self._LINESPACE for i in range(ticks)]
                elif y > self.tmax-0.5*self._LINESPACE:
                    ticks = (y - self.tmax) // self._LINESPACE
                    tick_ylist = [self.tmax + (i+1)*self._LINESPACE for i in range(ticks)]
                if ticks:
                    for tick_y in tick_ylist:
                        line = ax.axhline(tick_y,
                                   xmin=(x-.75*self._LINESPACE)/xspan, 
                                   xmax=(x+.75*self._LINESPACE)/xspan, 
                                   c='k')
                        self.drawings.append(line)

            # line = None
            # if y in self.bass_range:
                # if y < self.bmin-0.5*self._LINESPACE or y > self.bmax-0.5*self._LINESPACE:
                    # line = ax.axhline(y,
                               # xmin=(x-.75*self._LINESPACE)/xspan, 
                               # xmax=(x+.75*self._LINESPACE)/xspan, 
                               # c='k')
                
            # if y in self.treb_range:
                # if y < self.tmin-0.5*self._LINESPACE or y > self.tmax-0.5*self._LINESPACE:
                    # line = ax.axhline(y,
                               # xmin=(x-.75*self._LINESPACE)/xspan, 
                               # xmax=(x+.75*self._LINESPACE)/xspan, 
                               # c='k')
            
            # if line:
                # self.drawings.append(line)
        
            
    def get_rand_note(self):
        """
        Generate a psuedo-random note
        
        Returns:
            y,note: the vertical position on the staff and the note name 
        """
        
        # flip a coin to choose bass or treble
        if rand.random() > 0.5:
            idcs = self.bass_range
            note_func = self.bass_y
        else:
            idcs = self.treb_range
            note_func = self.treb_y

        y = rand.choice(idcs)
        return (y, note_func(y))

    def clear_drawings(self):
        """
        purge the drawn elements from the plot
        """
        for elem in self.drawings:
            elem.remove()
        self.drawings = []

    # TODO: delete if not useful
    def onkeypress(self, event):
        """ Get keypress and set direction of snake movement if an arrowkey is 
            pressed. dir is set to the index of DIR corresponding to the correct
            increment. Numbers 0-3 are used to distinguish directionaliy. Disallow
            antiparallel direction changes, e.g. right to left. 
        """
        global note
        
        # print('key pressed: ', event.key)
        key = event.key
        
        # check for direction changes
        if key ==  note.lower():
            self.advance = True
        
        elif key == 'q':
            self.running = False
            
    def record_result():
        # could write answers and responses to file for generating
        # learning stats
        pass


if __name__ == '__main__':

    sheet = Sheetly()
    fig, ax = sheet.draw_staff()
    fig.canvas.set_window_title(f'Sheetly v{sheet.VERSION}')
    fig.canvas.draw()

    plt.show(block=False)

    cheats = input ("show cheats in console? y for yes, anything else for no.")
    if cheats == 'y':
        cheats = True
    else:
        cheats = False

    print("type q to quit at any time.")

    running = True
    while running:
    
        time.sleep(0.1)
        # show the plot, await a response. 
        y,note = sheet.get_rand_note()
        if cheats:
            print(note)
        sheet.draw_notes([y],ax)
        fig.canvas.draw()
        response = input("note is:")

        if str(response).lower() == note[0].lower():
            ax.set_title('GOOD!', c='g')
        elif str(response).lower() == 'q':
            running = False
        else:
            ax.set_title(f'OOPS...{note}', c='r')
            
        sheet.clear_drawings()
        fig.canvas.flush_events()
        