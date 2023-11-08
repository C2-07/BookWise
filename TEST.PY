import matplotlib.pyplot as plt
import numpy as np
x = [1,2,3,4,5]
y = [5,6,7,8,9]

plt.barh(x,y)
plt.yticks(np.arange(1,6),["A",'B',"C",'D',"E"])
plt.show()
