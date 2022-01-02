import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

x=np.linspace(0,1,1400)
y=7*np.sin(2*np.pi*200*x) + 5*np.sin(2*np.pi*400*x)+3*np.sin(2*np.pi*600*x)

plt.figure()
plt.plot(x,y)
plt.title('initial')

plt.figure()
plt.plot(x[0:50],y[0:50])
plt.title('initial50')
plt.show()

fft_y=fft(y)
print(len(fft_y))
print(fft_y[0:5])