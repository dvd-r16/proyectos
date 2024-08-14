import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 2 * np.pi, 0.01)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel('0 a 2*pi') 
plt.ylabel('sin(x)')                   
plt.title('sin(x)')            
plt.grid(True)                           
plt.show()