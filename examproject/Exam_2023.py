import sympy as sm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from types import SimpleNamespace

class Model:
    def figure_1(x1,x2,x3):
        plt.plot(x1, x2)
        plt.xlabel(x3[0])
        plt.ylabel(x3[1])
        plt.title(f'Optimal {x3[1]} vs. {x3[0]}')

    def PrintOpt(x1,x2):
        x3= max( (v, i) for i, v in enumerate(x2) )
        print(f"The optimum is found in the tax rate iteration {x3[1]}. The optimal tax rate is {x1[x3[1]]:.3f}, that is {x1[x3[1]]*100:.0f}%. At this rate the utility is maximized at {x3[0]:.3f}.")



    def figure_3(x_k0_values):
        x_k0_values=np.array(x_k0_values)
        N = np.arange(len(x_k0_values))
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1,projection='3d')
        cs = ax.scatter(x_k0_values[:,0],x_k0_values[:,1],N,c=N);        

        # b. add labels
        ax.set_xlabel('$x_1$')
        ax.set_ylabel('$x_2$')
        ax.set_zlabel('$Iter$')

        # c. invert xaxis
        ax.invert_xaxis()

        # d. colorbar
        fig.colorbar(cs);
                