import sympy as sm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from types import SimpleNamespace

class Figures:
    def figure_1(x1,x2,x3):
        plt.plot(x1, x2)
        plt.xlabel(x3[0])
        plt.ylabel(x3[1])
        plt.title(f'Optimal {x3[1]} vs. {x3[0]}')


    def figure_3(x_k0_values):
        x_k0_values=np.array(x_k0_values)
        N = np.arange(len(x_k0_values))
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1,projection='3d')
        cs = ax.scatter(x_k0_values[:,0],x_k0_values[:,1],N,c=N);        

        # b. add labels
        ax.set_xlabel('$x_1$')
        ax.set_ylabel('$x_2$')
        ax.set_zlabel('$Iteration$')

        # c. invert xaxis
        ax.invert_xaxis()

        # d. colorbar
        fig.colorbar(cs);
                