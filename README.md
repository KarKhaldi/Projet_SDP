# Planification_Et_Affectation
Either the notebook or the main.py file can be used to solve the problem. However, we recommand using the notebook for a more step-by-step solving.

Solving a multi-objective planning problem using the Gurobi linear solver.

The data folder has example datasets with lists of workers and jobs. The objective is to find a planning to optimize multiple objectives:

Maximize the total money generated (gain - penalties of jobs taken)
Minimize the maximum amount of different jobs assigned to a worker
Minimize the maximum duration of a project
The model used here is explained in the report.pdf file.

Here is the Surface of solutions of the planning problem on the small data instance, it reprensents non-dominated solutions to the problem as red dots i.e 
<p align="center">
  <img src="results\toy_instance\newplot.png" alt="Pareto Surface" width="80%"/>
</p>


We can choose solutions according to this plot. For example, we can get this planning:

<p align="center">
  <img src="results\toy_instance\1.png" alt="Example Solution" width="80%"/>
</p>


And finally, we can rank our solutions using the function given in preferences.py and get rankings using Weighted Sum Models and TOPSIS such as :

<p align="center">
  <img src="results\large_instance\good_solution_ranking.png" alt="Example Solution" width="80%"/>
</p>
