import sys 
from model.generate_model import *
from model.plotting_solutions import *

# Opening JSON file
instance_name = "./data/medium_instance"
f = open(instance_name+".json")
# returns JSON object as a dictionary
data = json.load(f)


## Problem's parameters :

S = len(data["staff"]) # Number of individuals
H = data["horizon"]+1 # Horizon
J = len(data["jobs"]) # Number of projects
Q = len(data["qualifications"]) # Number of qualifications



solution_dict = solver_model(data,S,H,J,Q)
solution_reduite = reduce_solution_format(solution_dict)
non_dominated_sol = get_non_dominated_solutions(solution_reduite)

#example of plotting of ranking :

plotting_figure(non_dominated_sol,solution_dict)