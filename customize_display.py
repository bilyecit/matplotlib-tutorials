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
        self.lineStyle = QComboBox()
        self.lineStyle.addItems(['==line style==','-', '--', '-.', ':'])
        self.lineColor = QComboBox()
        self.lineColor.addItems(['==line color==','red', 'green','blue', 'yellow'])
        self.lineAlpha = QSlider(Qt.Horizontal)
        self.lineAlpha.setRange(1,10)
        self.lineAlpha.setSingleStep(1)
        self.lineWidth = QSlider(Qt.Horizontal)
        self.lineWidth.setRange(1,20)
        self.lineWidth.setSingleStep(1)
        
        self.lineStyle.currentTextChanged[str].connect(self.lineStyleChanged)
        self.lineColor.currentTextChanged[str].connect(self.lineColorChanged)
        self.lineAlpha.valueChanged[int].connect(self.lineAlphaChanged)
        self.lineWidth.valueChanged[int].connect(self.lineWidthChanged)
        
        tlayout = QVBoxLayout()
        tlayout.addWidget(self.lineStyle)
        tlayout.addWidget(self.lineColor)
        tlayout.addWidget(self.lineAlpha)
        tlayout.addWidget(self.lineWidth)
        topGroup.setLayout(tlayout)
        
        legendGroup = QGroupBox("legend-control")
        lgdLayout = QVBoxLayout()
        self.legend_visiable = QCheckBox('visible')
        self.legend_visiable.setChecked(True)
        self.lgdPos = QComboBox()
        self.lgdPos.addItems(['==legend loc==','best',
                'upper right',
                'upper left',
                'lower left' ,
                'lower right',
                'right',
                'center left',
                'center right',
                'lower center',
                'upper center',
                'center' ])
        lgdLayout.addWidget(self.legend_visiable)
        lgdLayout.addWidget(self.lgdPos)
        self.legend_visiable.clicked[bool].connect(self.legend_visible)
        self.legend_visiable.clicked[bool].connect(self.lgdPos.setEnabled)
        self.lgdPos.currentTextChanged[str].connect(self.setLegendPosition)
        legendGroup.setLayout(lgdLayout)
        
        leftGroup = QGroupBox("left-axis")
        self.l_check = QCheckBox("visible")
        self.l_check.setChecked(True)
        self.l_check.clicked[bool].connect(self.left_axis_visiable)
        self.l_position = QSlider(Qt.Horizontal)
        self.l_position.setRange(-3,3)
        self.l_position.setSingleStep(1)
        self.l_position.valueChanged[int].connect(self.left_axis_position_changed)
        llayout = QVBoxLayout()
        llayout.addWidget(self.l_check)
        llayout.addWidget(self.l_position)
        leftGroup.setLayout(llayout)
        
        bottomGroup = QGroupBox("bottom-axis")
        self.b_check = QCheckBox("visible")
        self.b_check.setChecked(True)
        self.b_check.clicked[bool].connect(self.bottom_axis_visiable)
        self.b_position = QSlider(Qt.Horizontal)
        self.b_position.setRange(-1,1)
        self.b_position.setSingleStep(1)
        self.b_position.valueChanged[int].connect(self.bottom_axis_position_changed)
        blayout = QVBoxLayout()
        blayout.addWidget(self.b_check)
        blayout.addWidget(self.b_position)
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
        line = event.artist
        self.picked_line = line
        style, color, alpha, width = line.get_linestyle(),line.get_color(),line.get_alpha(),line.get_linewidth()
        self.updateLineInfos(style, color, alpha, width)
    
    def draw(self):
        self.ax = self.mainfigure.add_subplot(111)
        x = np.linspace(-np.pi, np.pi, 256,endpoint=True)
        line = self.ax.plot(x, np.sin(x), color='red' , label='sin(x)', picker=5, linewidth=1.0)
        self.line_sin = line[0]
        line = self.ax.plot(x, np.cos(x), color='blue' , label='cos(x)', linewidth=1.0)
        self.line_cos = line[0]
        self.line_cos.set_picker(5)
        self.picked_line = self.line_sin
        self.ax.legend(loc='best')
        lgd_lc, lgd_ls = self.ax.get_legend().get_lines()
        lgd_lc.set_picker(2)
        lgd_ls.set_picker(2)
        
        self.ax.set_xlim(x.min()*1.1, x.max()*1.1)
        self.ax.set_ylim(-1.1, 1.1)
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        self.ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
        self.ax.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
        self.ax.set_yticks([-1, +1])
        self.ax.set_yticklabels([r'$-1$', r'$+1$'])
        
        self.ax.spines['left'].set_position(('data', self.l_position.value()))
        self.ax.spines['bottom'].set_position(('data', self.b_position.value()))
        
        self.ax.set_title('This is Figure Title:\nmatplotlib demo', color='magenta')
        #self.ax.set_xlabel('This X label', color='magenta')
        #self.ax.set_ylabel('This is y label', color='magenta')
        
    def left_axis_visiable(self,  visible):
        self.ax.spines['left'].set_visible(visible)
        self.updateData()

    def left_axis_position_changed(self, val):
        self.ax.spines['left'].set_position(('data', val))
        self.updateData()
    
    def bottom_axis_visiable(self,  visible):
        self.ax.spines['bottom'].set_visible(visible)
        self.updateData()

    def bottom_axis_position_changed(self, val):
        self.ax.spines['bottom'].set_position(('data', val))
        self.updateData()
        
    def legend_visible(self, visible):
        lgd = self.ax.get_legend()
        lgd.set_visible(visible)
        self.updateData()
    
    def setLegendPosition(self, pos):
        if pos == '==legend loc==':
            return
        self.ax.legend(loc=pos)
        self.mainCanvas.draw()
        
    def lineStyleChanged(self, style):
        if style == '==line style==':
            return
        if self.picked_line:
            self.picked_line.set_linestyle(style)
        self.updateData()
    
    def lineColorChanged(self, color):
        if color == "==line color==":
            return
        if self.picked_line:
            self.picked_line.set_color(color)
            self.updateData()
        
    def lineAlphaChanged(self, val):
        val /= 10
        self.picked_line.set_alpha(val)
        self.updateData()
        
    def lineWidthChanged(self, val):
        val /= 2
        self.picked_line.set_linewidth(val)
        self.updateData()
    
    def updateLineInfos(self, style, color, alpha, width):
        lineStyleList = ['==line style==','-', '--', '-.', ':']
        lineColorList = ['==line color==','red', 'green','blue', 'yellow']
        self.lineStyle.setCurrentIndex(lineStyleList.index(style))
        self.lineColor.setCurrentIndex(lineColorList.index(color))
        if alpha == None:
            self.lineAlpha.setValue(self.lineAlpha.maximum())
        else:
            self.lineAlpha.setValue(int(alpha*10))
            
        self.lineWidth.setValue(int(2*width))

    def updateData(self):
        self.mainCanvas.draw()

def main():
    app = QApplication(sys.argv)
    cui= CustomizeAxes()
    cui.show()
    return sys.exit(app.exec_())

if __name__ == '__main__':
    main()
