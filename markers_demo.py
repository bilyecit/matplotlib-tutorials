import matplotlib.pyplot as plt
import numpy as np

def pickEvent(event):
    obj = event.artist
    obj.set_edgecolor('red')
    obj.set_alpha(1)
    obj.set_sizes([100])
    plt.gcf().canvas.draw()


def show_marker_styles():
    marker_style_list=['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_']
    xy_ticks = np.arange(np.shape(marker_style_list)[0])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.canvas.mpl_connect('pick_event', pickEvent)
    
    for mrk,xy_tick in zip(marker_style_list, xy_ticks):
        sct = ax.scatter(xy_tick, xy_tick, marker=mrk, alpha=0.5, picker=5)
        #sct.set_picker(5)
    
    plt.show()

def main():
    show_marker_styles()


if __name__ == '__main__':
    main()
