import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mpw
import tkinter.filedialog as tk
from tkinter import filedialog
from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import BasicAlgorithms as BA

class Index(object):
    ind = 0

    def quit(event):
        fenetre_sequences.quit()
        plt.close()

    def plot(self, event):
        if event.x >91 and event.x < 330 and event.y > 59 and event.y < 436:
            global ax
            m_x, m_y = event.x, event.y
            ix, iy = ax.transData.inverted().transform([m_x, m_y])
            ax.plot(ix, iy, marker='o')
            global fig
            fig.canvas.draw()
            adding_sequence(list_sequences, ix, iy)

def create_window():
    global textfield_results
    global fenetre_sequences

    fenetre_sequences = tk.Tk()
    fenetre_sequences.geometry("400x300")
    fenetre_sequences.title("Random sequences")
    fenetre_sequences['bg'] = 'silver'
    scrollbar_result = tk.Scrollbar(fenetre_sequences)
    scrollbar_result.pack(side=RIGHT, fill=Y)
    textfield_results = tk.Text(fenetre_sequences, yscrollcommand=scrollbar_result.set, width=55)
    textfield_results.pack(padx=2)



def random_sequences():

    create_window()

    callback = Index()

    global list_sequences
    list_sequences = []
    global ax
    global fig
    fig = plt.figure(figsize=(7,5), dpi=100)
    ax = fig.add_subplot(121)
    fig.canvas.mpl_connect('button_press_event', callback.plot)

    ax_button_quit = plt.axes([0.89, 0.02, 0.1, 0.075])
    button_quit = mpw.Button(ax_button_quit, 'Save and quit')
    button_quit.label.set_fontsize(6.5)
    button_quit.on_clicked(callback.quit)

    plt.show()

    return list_sequences


if __name__ == '__main__':
    print(random_sequences())
