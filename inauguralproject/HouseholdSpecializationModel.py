
from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdSpecializationModelClass:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()
        # b. preferences
        par.rho = 2.0
        par.nu = 0.001
        par.epsilon = 1.0
        par.omega = 0.5 
    
        # c. household production
        par.alpha = 0.5
        par.sigma = 1

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)

        # e. targets
        par.beta0_target = 0.4
        par.beta1_target = -0.1

        # f. res
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        #Sigma is not 0 so this option is not created
        if par.sigma==1:
            H = HM**(1-par.alpha)*HF**par.alpha
        else :
            #Add 1e-8 to stop boundary error
            H = ((1e-8+1-par.alpha)*HM**((1e-8+par.sigma-1)/par.sigma)+par.alpha*HF**((1e-8+par.sigma-1)/par.sigma))**((1e-8+par.sigma)/(par.sigma-1))
        
        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        #Add 1e-8 to stop boundary error
        utility = np.fmax(Q,1e-8)**(1e-8+1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        #Add 1e-8 to stop error
        x = np.linspace(0+1e-8,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self,do_print=False):
        """ solve model continously """
       
        opt = SimpleNamespace()

        #define constraints
        def constraints(x) :
            {'type': 'ineq', 'fun': lambda x: 24- x[0]-x[1]}, 
            {'type': 'ineq', 'fun': lambda x: 24- x[0]-x[1]}
        
        #define bounds
        #Add 1e-8 to stop error
        bounds = [(0+1e-8,24)] * 4

        # initial guess
        initial_guess = [3, 3, 3, 3]

        # define objective_function function
        def objective_function(x):
            LM, HM, LF, HF = x
            return -self.calc_utility(LM, HM, LF, HF)
        
        # solve for optimum
        res = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)
        
        opt.LM, opt.HM, opt.LF, opt.HF = res.x

        return opt

    def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """
    
        par = self.par
        sol = self.sol

        for x, wF in enumerate(par.wF_vec):
            par.wF = wF
            results = self.solve()
            sol.HF_vec[x] = results.HF
            sol.HM_vec[x] = results.HM
            sol.LF_vec[x] = results.LF
            sol.LM_vec[x] = results.LM
            
        return sol.HF_vec, sol.HM_vec, sol.LF_vec, sol.LM_vec


    def run_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol
        
        self.solve_wF_vec()

        x = np.log(par.wF_vec)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T

        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]

        return sol.beta0,sol.beta1
    
    def estimate(self,alpha=None,sigma=None):
        """ estimate alpha and sigma """

        par = self.par
        sol = self.sol

        # define objective_function function to minimize
        def objective_function(x):
            par.alpha, par.sigma = x
            self.solve_wF_vec()
            self.run_regression()
            return (par.beta0_target - sol.beta0)**2+(par.beta1_target - sol.beta1)**2
        
        # initial guess
        initial_guess = [0.5, 1.0]

        # solve for optimum
        res = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead')

        alpha_min, sigma_min = res.x

        return alpha_min, sigma_min 
    
class Figure:

    
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.title = "x"

    def plot(self, ratioW, ratioH, f=None):
        #Make the standard plot
        self.ax.plot(ratioW, ratioH, label="Model", color='black')
        #If statement that makes the class usable in all the plots
        if f is not None:
            self.ax.scatter(ratioW, f, label="Siminski and Yetsenga")
        else:
            pass
        self.ax.set_xlabel("log(WF/WM)")
        self.ax.set_ylabel("log(HF/HM)")
        self.ax.set_title(self.title)
        self.ax.legend()
        plt.show()
