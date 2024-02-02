# Required installs:
    # pip install PyQt5
    # pip install pyqtgraph
   
# References:
    # https://www.brown.edu/research/labs/mittleman/sites/brown.edu.research.labs.mittleman/files/uploads/lecture15_6.pdf
    # https://en.wikipedia.org/wiki/Jones_calculus
    # Hecht Optics
    # Pedtrotti Intro to Optics
    # https://demonstrations.wolfram.com/PolarizationOfLightThroughAWavePlate/
   
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QLineEdit, QSpinBox, QCheckBox
import pyqtgraph as pg
import scipy.constants as pc
from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.widget = QtWidgets.QWidget()        
        plot_win = pg.GraphicsLayoutWidget()  
        plot_win.setBackground('w')
        self.plot1 = plot_win.addPlot(row = 0, col = 0)
        self.plot1.setAspectLocked(1)
        self.plot2 = plot_win.addPlot(row = 0, col = 1)
        self.plot2.setAspectLocked(1)

        self.styles = {'color':'b', 'font-size':'20px'} # style for labels
        self.plot1.setLabel('left', 'E 0°', **self.styles) # labels for plots
        self.plot1.setLabel('bottom', 'E 90°', **self.styles)
        self.plot1.setLabel('top', 'Polarization before Waveplate', **self.styles)
        self.plot2.setLabel('left', 'E 0°', **self.styles)
        self.plot2.setLabel('bottom', 'E 90°', **self.styles)
        self.plot2.setLabel('top', 'Polarization after Waveplate', **self.styles)
        self.plot1.setXRange(-1, 1)
        self.plot1.setYRange(-1, 1)
        self.plot2.setXRange(-1, 1)
        self.plot2.setYRange(-1, 1)

        self.pen = pg.mkPen(color=(255, 0, 0))
        self.data_line1 =  self.plot1.plot([0], [0], pen = self.pen)
        self.data_line2 =  self.plot2.plot([0], [0], pen = self.pen)  
        self.lm = 500*10**-9 # wavelength of light, m
        self.w = 2*np.pi*pc.c/self.lm  # angular frequency, omega, of light, Hz
        self.n = np.pi/2 # phase retardation of the waveplate (e.g. for a QWP, n=np.pi/2, for a HWP, n=np.pi)
        self.t = np.linspace(0, 2*np.pi/self.w) # time wave propagates for a 2*pi cycle, s

        def valueenter0():
            try:
                self.n = float(self.lineedit0.text()) * np.pi
            except:
                self.lineedit0.clear()
                self.lineedit0.setPlaceholderText('Enter valid float')
   
        def valueenter1():
            try:
                self.slider.setValue(int(self.lineedit1.text()))
            except:
                self.lineedit1.clear()
                self.lineedit1.setPlaceholderText('Enter Valid Degree Angle (int)°')

        def valueenter2():
            try:
                self.slider2.setValue(int(self.lineedit2.text()))
            except:
                self.lineedit2.clear()
                self.lineedit2.setPlaceholderText('Enter Valid Degree Angle (int)°')
               
        self.lineedit0 = QLineEdit()
        self.lineedit0.setPlaceholderText("Phase retardation, default QWP 0.5")
        self.lineedit0.setAlignment(QtCore.Qt.AlignLeft)
        self.lineedit0.setMaximumWidth(250)
        self.lineedit0.editingFinished.connect(valueenter0)  
        self.lineedit0.editingFinished.connect(self.plot)
        self.lineedit1 = QLineEdit()
        self.lineedit1.setPlaceholderText("Angle° (int)")
        self.lineedit1.setAlignment(QtCore.Qt.AlignLeft)
        self.lineedit1.setMaximumWidth(250)
        self.lineedit1.editingFinished.connect(valueenter1)
        self.lineedit2 = QLineEdit()
        self.lineedit2.setPlaceholderText("Angle ° (int)")
        self.lineedit2.setMaximumWidth(250)  
        self.lineedit2.editingFinished.connect(valueenter2)
       
        self.labela = QLabel("Enter A*100 > 0")
        self.labela.setAlignment(QtCore.Qt.AlignCenter)
        self.labelb = QLabel("Enter B*100")
        self.labelb.setAlignment(QtCore.Qt.AlignCenter)
        self.labelc = QLabel(U"Enter C*100 (Handedness: C<0 \u22B2-- RH, C>0  --\u22B3 LH)")
        self.labelc.setAlignment(QtCore.Qt.AlignCenter)  
        self.spina = QSpinBox()
        self.spina.setAlignment(QtCore.Qt.AlignLeft)
        self.spina.setMaximumWidth(50)
        self.spina.setMaximum(1000)
        self.spina.editingFinished.connect(self.plot)
        self.spina.valueChanged.connect(self.plot)
        self.spinb = QSpinBox()
        self.spinb.setAlignment(QtCore.Qt.AlignLeft)
        self.spinb.setMaximumWidth(50)
        self.spinb.setMaximum(1000)
        self.spinb.setMinimum(-1000)
        self.spinb.editingFinished.connect(self.plot)
        self.spinb.valueChanged.connect(self.plot)
        self.spinc = QSpinBox()
        self.spinc.setAlignment(QtCore.Qt.AlignLeft)
        self.spinc.setMaximumWidth(50)
        self.spinc.setMaximum(1000)
        self.spinc.setMinimum(-1000)
        self.spinc.editingFinished.connect(self.plot)
        self.spinc.valueChanged.connect(self.plot)        
       
        self.labeleq = QLabel(U"Use elliptical polarization Jones vector: 1/(\u221A (A^2 + B^2 + C^2)) * [[A]  [B+iC]]")
        self.labeleq.setAlignment(QtCore.Qt.AlignRight)
        self.labeleq.setMaximumWidth(self.labeleq.width())
        self.polbox = QCheckBox()
        self.polbox.stateChanged.connect(self.plot)
       
        hlayout0 = QHBoxLayout()
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()
        hlayout4 = QHBoxLayout()
       
        self.slider = QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setValue(0)
        self.slider.setMinimum(0)
        self.slider.setMaximum(360)  
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.label0 = QLabel(U"Waveplate phase retardation x \u03C0: ")
        self.label0.setAlignment(QtCore.Qt.AlignCenter)
        self.label1 = QLabel("Angle of light polarization 0-360°: " + str(self.slider.value()) + '°')
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
       
        hlayout0.addWidget(self.label0)
        hlayout0.addWidget(self.lineedit0)        
        hlayout1.addWidget(self.label1)
        hlayout1.addWidget(self.lineedit1)
        hlayout2.addWidget(self.label2)
        hlayout2.addWidget(self.lineedit2)
        hlayout3.addWidget(self.labela)
        hlayout3.addWidget(self.spina)
        hlayout3.addWidget(self.labelb)
        hlayout3.addWidget(self.spinb)
        hlayout3.addWidget(self.labelc)
        hlayout3.addWidget(self.spinc)
        hlayout4.addWidget(self.labeleq)
        hlayout4.addWidget(self.polbox)
       
        layout = QVBoxLayout()
        layout.addWidget(plot_win)
        layout.addLayout(hlayout0)
        layout.addLayout(hlayout1)
        layout.addWidget(self.slider)
        layout.addLayout(hlayout2)
        layout.addWidget(self.slider2)
        layout.addLayout(hlayout3)
        layout.addLayout(hlayout4)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.plot()

    def plot(self):
       
        self.lp = self.slider.value()/360*2*np.pi # angle of laser linear polarization, measured in radians from horizontal axis
        self.h = self.slider2.value()/360*2*np.pi # angle of fast axis of the waveplate, measured in radians from horizontal axis    
        self.label1.setText('Angle of light polarization 0-360°: ' + str(self.slider.value()) + '°')
        self.label2.setText('Angle of fast axis of waveplate 0-360°: ' + str(self.slider2.value()) + '°')
       
        self.a = self.spina.value()/100
        self.b = self.spinb.value()/100
        self.c = self.spinc.value()/100
       
        if self.polbox.isChecked() == False:
           
            xlp = np.real(np.exp(1.j*self.w*self.t)*np.cos(self.lp))
            ylp = np.real(np.exp(1.j*self.w*self.t)*np.sin(self.lp))
            self.plot1.setLabel('bottom', 'E 90°', **self.styles)
            self.data_line1.setData(xlp, ylp, pen = self.pen)

        else:

            if self.spina.value() == self.spinb.value() == self.spinc.value() == 0:
                self.data_line1.setData([0], [0], pen = self.pen)
           
            else:

                xlp = np.real(np.exp(-1.j*self.w*self.t)*self.a/np.sqrt(self.a**2+self.b**2+self.c**2))
                ylp = np.real(np.exp(-1.j*self.w*self.t)*(self.b + 1.j*self.c)/np.sqrt(self.a**2+self.b**2+self.c**2))                
               
                if self.spina.value() == 0:
                   
                    self.plot1.setLabel('bottom', 'E 90°', **self.styles)
                   
                else:
                    if self.spinc.value() > 0:
                        self.plot1.setLabel('bottom', U'E 90° --\u22B3 LH', **self.styles)
                       
                    elif self.spinc.value() < 0:
                        self.plot1.setLabel('bottom', U"E 90° \u22B2-- RH", **self.styles)
       
                    else:
                        self.plot1.setLabel('bottom', 'E 90°', **self.styles)
               
                self.data_line1.setData(xlp, ylp, pen = self.pen) # these update the data


        if self.polbox.isChecked() == False:
           
            xeeo = np.real(np.exp(-1.j*self.w*self.t)*np.exp(-1.j*self.n/2)*(np.cos(self.lp)*((np.cos(self.h))**2+np.exp(1.j*self.n)*(np.sin(self.h))**2)+(1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*np.sin(self.lp)))
            yeeo = np.real(np.exp(-1.j*self.w*self.t)*np.exp(-1.j*self.n/2)*((1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*np.cos(self.lp)+((np.sin(self.h))**2+np.exp(1.j*self.n)*(np.cos(self.h))**2)*np.sin(self.lp)))
           
            img_part = np.imag(((1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*np.cos(self.lp)+((np.sin(self.h))**2+np.exp(1.j*self.n)*(np.cos(self.h))**2)*np.sin(self.lp))/((np.cos(self.lp)*((np.cos(self.h))**2+np.exp(1.j*self.n)*(np.sin(self.h))**2)+(1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*np.sin(self.lp))))

            if img_part > 0:
                self.plot2.setLabel('bottom', U'E 90° --\u22B3 LH', **self.styles)
                   
            elif img_part < 0:
                self.plot2.setLabel('bottom', U"E 90° \u22B2-- RH", **self.styles)
   
            else:
                self.plot2.setLabel('bottom', 'E 90°', **self.styles)
           
            self.data_line2.setData(xeeo, yeeo, pen = self.pen)

        else:
           
            if self.a == self.b == self.c == 0:
                self.data_line2.setData([0], [0], pen = self.pen)
               
            else:
               
                xeeo = np.real(np.exp(-1.j*self.w*self.t)*np.exp(-1.j*self.n/2)*(self.a*((np.cos(self.h))**2+np.exp(1.j*self.n)*(np.sin(self.h))**2)+(1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*(self.b + 1.j*self.c))/np.sqrt(self.a**2+self.b**2+self.c**2))
                yeeo = np.real(np.exp(-1.j*self.w*self.t)*np.exp(-1.j*self.n/2)*((1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*self.a+((np.sin(self.h))**2+np.exp(1.j*self.n)*(np.cos(self.h))**2)*(self.b + 1.j*self.c))/np.sqrt(self.a**2+self.b**2+self.c**2))                
               
   
                img_part = np.imag((((1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*self.a+((np.sin(self.h))**2+np.exp(1.j*self.n)*(np.cos(self.h))**2)*(self.b + 1.j*self.c)))/((self.a*((np.cos(self.h))**2+np.exp(1.j*self.n)*(np.sin(self.h))**2)+(1-np.exp(1.j*self.n))*np.cos(self.h)*np.sin(self.h)*(self.b + 1.j*self.c))))
   
                if img_part > 0:
                    self.plot2.setLabel('bottom', U'E 90° --\u22B3 LH', **self.styles)
                       
                elif img_part < 0:
                    self.plot2.setLabel('bottom', U"E 90° \u22B2-- RH", **self.styles)
       
                else:
                    self.plot2.setLabel('bottom', 'E 90°', **self.styles)
   
                self.data_line2.setData(xeeo, yeeo, pen = self.pen)
                
        # print((yeeo[:-1]**2-xeeo[:-1]**2).mean())  # see difference in intensities verical - horizontal, after waveplate
        # Maybe this will be incorporated into the GUI and plots at some point
    
    def closeEvent(self, event): # when window is closed
        super(MainWindow, self).closeEvent(event)
        app.quit()
        print('\nApp ended.')
   
if __name__ == '__main__':
       
    app = QApplication(sys.argv)  
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
