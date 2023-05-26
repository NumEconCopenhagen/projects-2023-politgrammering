# Examination project
In this project we have been given three problems. The first one being "optimal taxation with government spending" where given a utility function and parameters we find the social optimal tax rate and government consumption. Here we generally find that a tax rate of 0.5 will make government spendig, optimal utlity and optimal social utility the highest, with different parameters for the latter.

In the second problem, "Labor adjustment costs" we simulate a dynamic version of a profit maximization problem where a hair salon chooses the optimal amount of hairdressers. The optimal amount of hairdressers depends on the demand shocks, which takes an AR(1) process. In the model, it is costly to hire and fire hairdressers. We find that it is optimal to leave the number of hairdressers fixed when the change in hairdressers from the previous period is below delta=0.13. Finally, we investigate a new policy where the optimal number of hairdressers is fixed when the absolute value of the demand shocks is small. 

In the third problem, "Global optimizer with refined muliti-start", we consider a Griewank function where we use the refined global optimizer with multi-start to see how long it takes to converge towards the global minimum with different warm-up iterations. We find that the total interation counter is much larger with more warm-up interations meaning there is slower convergence with more warm-up iterations.


The **results** of the project can be seen from running [Exam-2023-notebook.ipynb] [here](Exam-2023-notebook.ipynb)

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires no further packages.
