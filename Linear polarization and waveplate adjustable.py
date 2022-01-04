import numpy as np
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
import scipy.constants as pc
from PyQt5 import QtCore


class Window(QDialog): 
       
    def __init__(self, parent=None): 
        super(Window, self).__init__(parent) 
    
        self.figure = Figure(figsize = (12, 8))  
        self.canvas = FigureCanvas(self.figure) 
        self.toolbar = NavigationToolbar(self.canvas, self) 
        
        self.lm = 800*10**-9 #wavelength of laser, m
        self.w = 2*np.pi*pc.c/self.lm  #angular frequency, omega, of laser, Hz
        self.n = np.pi/2 #phase retardation of the waveplate (e.g. for a QWP, n=np.pi/2, for a HWP, n=np.pi)
        self.t = np.linspace(0,2*np.pi/self.w) #time wave propagates for a 2*pi cycle, s

        def valueenter1():
            try:
                self.slider.setValue(int(self.lineedit1.text()))
            except:
                self.lineedit1.setText('Enter Valid Degree Angle °')

        def valueenter2():
            try:
                self.slider2.setValue(int(self.lineedit2.text()))
            except:
                self.lineedit2.setText('Enter Valid Degree Angle °')
        
        self.lineedit1 = QLineEdit("Enter Angle°")
        self.lineedit1.setAlignment(QtCore.Qt.AlignLeft)
        self.lineedit1.setMaximumWidth(200)
        self.lineedit1.editingFinished.connect(valueenter1)
        self.lineedit2 = QLineEdit("Enter Angle °")
        self.lineedit2.setMaximumWidth(200)  
        self.lineedit2.editingFinished.connect(valueenter2)
            
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()

        self.slider = QSlider() 
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setValue(0)
        self.slider.setMinimum(0) 
        self.slider.setMaximum(360)  
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.label1 = QLabel("Angle of laser polarization 0-360°: " + str(self.slider.value()) + '°')
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.slider.valueChanged.connect(self.plot) 
        
        self.slider2 = QSlider() 
        self.slider2.setOrientation(QtCore.Qt.Horizontal) 
        self.slider2.setValue(45)
        self.slider2.setMinimum(0) 
        self.slider2.setMaximum(360) 
        self.slider2.setTickInterval(5)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.label2 = QLabel("Angle of fast axis of waveplate 0-360°: " + str(self.slider2.value()) + '°') 
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.slider2.valueChanged.connect(self.plot)
        
        hlayout1.addWidget(self.label1)
        hlayout1.addWidget(self.lineedit1)
        hlayout2.addWidget(self.label2)
        hlayout2.addWidget(self.lineedit2)
        
        layout = QVBoxLayout() 
        layout.addWidget(self.toolbar) 
        layout.addWidget(self.canvas) 
        layout.addLayout(hlayout1) 
        layout.addWidget(self.slider)
        layout.addLayout(hlayout2) 
        layout.addWidget(self.slider2)
        self.setLayout(layout)
        
        self.plot()

    def plot(self): 
   
        self.figure.clear() 
        
        self.lp = self.slider.value()/360*2*np.pi # angle of laser linear polarization, measured in radians from horizontal axis
        self.h = self.slider2.value()/360*2*np.pi # angle of fast axis of the waveplate, measured in radians from horizontal axis     
        self.label1.setText('Angle of fast axis of waveplate 0-360°: ' + str(self.slider.value()) + '°')
        self.label2.setText('Angle of fast axis of waveplate 0-360°: ' + str(self.slider2.value()) + '°')
        
        ax = self.figure.add_subplot(121, aspect = 'equal') 
        xlp = np.real(np.exp(-1.j*self.w*self.t)*np.cos(self.lp))
        ylp = np.real(np.exp(-1.j*self.w*self.t)*np.sin(self.lp))
        ax.plot(xlp,ylp)
        ax.set_xlabel('$E_{90^\circ}$')
        ax.set_ylabel('$E_{0^\circ}$')
        ax.set_title('Polarization before Waveplate')
        ax.axis([-1,1,-1,1])
        
        ax2 = self.figure.add_subplot(122, aspect = 'equal')
        xeeo = np.real(np.exp(-1.j*self.w*self.t)*(np.cos(self.lp)*(np.exp(1.j*self.n/2)*(np.cos(self.h))**2+np.exp(-1.j*self.n/2)*(np.sin(self.h))**2)+(-np.exp(-1.j*self.n/2)+np.exp(1.j*self.n/2))*np.cos(self.h)*np.sin(self.h)*np.sin(self.lp)))
        yeeo = np.real(np.exp(-1.j*self.w*self.t)*((-np.exp(-1.j*self.n/2)+np.exp(1.j*self.n/2))*np.cos(self.h)*np.cos(self.lp)*np.sin(self.h)+(np.exp(-1.j*self.n/2)*(np.cos(self.h))**2+np.exp(1.j*self.n/2)*(np.sin(self.h))**2)*np.sin(self.lp)))
        ax2.plot(xeeo,yeeo)
        ax2.set_xlabel('$E_{90^\circ}$')
        ax2.set_ylabel('$E_{0^\circ}$')
        ax2.set_title('Polarization after Waveplate')
        ax2.axis([-1,1,-1,1])

        self.canvas.draw() 
    
    
if __name__ == '__main__': 
       
    app = QApplication(sys.argv)  
    main = Window() 
    main.show() 
    sys.exit(app.exec_()) 
