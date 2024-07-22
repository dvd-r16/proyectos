import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 2 * np.pi, 0.01)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel('x values from 0 to 2*pi') 
plt.ylabel('sin(x)')                   
plt.title('Plot of sin(x)')            
plt.grid(True)                           
plt.show()