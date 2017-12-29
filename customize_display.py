import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
import numpy as np
from PyQt5.Qt import QMainWindow, QApplication, QVBoxLayout, QLabel, QComboBox,\
    QGridLayout, QHBoxLayout, QWidget, QGroupBox, QCheckBox, QSlider, Qt


class CustomizeAxes(QMainWindow):
    def __init__(self, parent=None):
        super(CustomizeAxes, self).__init__(parent)
        self.setupUis()
        self.draw()
    
    def setupUis(self):
        self.mainWidget = QWidget(self)
        
        self.mainfigure = plt.figure()
        self.mainCanvas = self.mainfigure.canvas
        self.mainCanvas.mpl_connect("pick_event", self.pick_event)
        
        topGroup = QGroupBox("line-styles")
        lineStyle = QComboBox()
        lineStyle.addItems(['==line style==','-', '--', '-.', ':'])
        lineColor = QComboBox()
        lineColor.addItems(['red', 'green','blue', 'yellow'])
        lineAlpha = QSlider(Qt.Horizontal)
        lineAlpha.setRange(1,10)
        lineAlpha.setSingleStep(1)
        
        lineStyle.currentTextChanged[str].connect(self.lineStyleChanged)
        lineColor.currentTextChanged[str].connect(self.lineColorChanged)
        lineAlpha.valueChanged[int].connect(self.lineAlphaChanged)
        
        tlayout = QVBoxLayout()
        tlayout.addWidget(lineStyle)
        tlayout.addWidget(lineColor)
        tlayout.addWidget(lineAlpha)
        topGroup.setLayout(tlayout)
        
        legendGroup = QGroupBox("legend-control")
        lgdLayout = QVBoxLayout()
        legend_visiable = QCheckBox('visible')
        lgdPos = QComboBox()
        lgdPos.addItems(['best',
                'upper right',
                'upper left',
                'lower left' ,
                'lower right' ,
                'right'           ,
                'center left'     ,
                'center right'   ,
                'lower center'   ,
                'upper center'   ,
                'center' ])
        lgdLayout.addWidget(legend_visiable)
        lgdLayout.addWidget(lgdPos)
        legend_visiable.clicked[bool].connect(self.legend_visible)
        legend_visiable.clicked[bool].connect(lgdPos.setEnabled)
        lgdPos.currentTextChanged[str].connect(self.legend_pos)
        legendGroup.setLayout(lgdLayout)
        
        leftGroup = QGroupBox("left-axis")
        l_check = QCheckBox("visible")
        l_check.clicked[bool].connect(self.left_axis_visiable)
        l_position = QSlider(Qt.Horizontal)
        l_position.setRange(-3,3)
        l_position.setSingleStep(1)
        l_position.valueChanged[int].connect(self.left_axis_position_changed)
        llayout = QVBoxLayout()
        llayout.addWidget(l_check)
        llayout.addWidget(l_position)
        leftGroup.setLayout(llayout)
        
        bottomGroup = QGroupBox("bottom-axis")
        b_check = QCheckBox("visible")
        b_check.clicked[bool].connect(self.bottom_axis_visiable)
        b_position = QSlider(Qt.Horizontal)
        b_position.setRange(-1,1)
        b_position.setSingleStep(1)
        b_position.valueChanged[int].connect(self.bottom_axis_position_changed)
        blayout = QVBoxLayout()
        blayout.addWidget(b_check)
        blayout.addWidget(b_position)
        bottomGroup.setLayout(blayout)
        
        self.ctrlLayout = QHBoxLayout()
        self.ctrlLayout.addWidget(topGroup)
        self.ctrlLayout.addWidget(legendGroup)
        self.ctrlLayout.addWidget(leftGroup)
        self.ctrlLayout.addWidget(bottomGroup)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.mainCanvas)
        self.mainLayout.addLayout(self.ctrlLayout)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    
    def pick_event(self, event):
        print(type(event))
    
    def draw(self):
        self.ax = self.mainfigure.add_subplot(111)
        x = np.linspace(-np.pi, np.pi, 256,endpoint=True)
        line = self.ax.plot(x, np.sin(x), color='r' , label='sin(x)', picker=5)
        self.line_sin = line[0]
        line = self.ax.plot(x, np.cos(x), color='b' , label='cos(x)' )
        self.line_cos = line[0]
        self.line_cos.set_picker(True)
        self.line_cos.set_picker(5)
        
        self.ax.legend(loc='best')
        
        self.ax.set_xlim(x.min()*1.1, x.max()*1.1)
        #self.ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2,np.pi],[r'$-np.pi$', r'$-np.pi/2$', r'$0$', r'$np.pi/2$', r'$np.pi$'])
        self.ax.set_ylim(-1.1, 1.1)
        #self.ax.set_yticks([-1, +1], [r'$-1$', r'$+1$'])
        #plt.show()
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        #self.ax.spines['left'].set_position(('data',0))
        #self.ax.spines['bottom'].set_position(('data',0))
        #plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
        #plt.yticks([-1, +1], [r'$-1$', r'$+1$'])
        
        self.ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
        self.ax.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
        self.ax.set_yticks([-1, +1])
        self.ax.set_yticklabels([r'$-1$', r'$+1$'])
        
    def left_axis_visiable(self,  visible):
        self.ax.spines['left'].set_visible(visible)
        self.mainCanvas.draw()

    def left_axis_position_changed(self, val):
        self.ax.spines['left'].set_position(('data', val))
        self.mainCanvas.draw()
    
    def bottom_axis_visiable(self,  visible):
        print('@bottom_axis_visiable', visible)
        self.ax.spines['bottom'].set_visible(visible)
        self.mainCanvas.draw()

    def bottom_axis_position_changed(self, val):
        self.ax.spines['bottom'].set_position(('data', val))
        self.mainCanvas.draw()
        
    def legend_visible(self, visible):
        lgd = self.ax.get_legend()
        lgd.set_visible(visible)
        self.mainCanvas.draw()
    
    def legend_pos(self, pos):
        self.ax.legend(loc=pos)
        self.mainCanvas.draw()
        
    def lineStyleChanged(self, style):
        if style == '==line style==':
            return
        self.line_cos.set_linestyle(style)
        self.mainCanvas.draw()
    
    def lineColorChanged(self, color):
        self.line_cos.set_color(color)
        self.mainCanvas.draw()
        
    def lineAlphaChanged(self, val):
        val = val/10
        self.line_cos.set_alpha(val)
        self.mainCanvas.draw()

def main():
    app = QApplication(sys.argv)
    cui= CustomizeAxes()
    cui.show()
    return sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    
