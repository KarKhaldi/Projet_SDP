import gurobipy
from gurobipy import *

from random import randint
import pandas as pd
import numpy as np
import json

# for creating a responsive plot

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

## def functions from json
def vacations(collaborator, day):
    if day in collaborator["vacations"]:
        return 1
    else:
        return 0
def has_qualification(collaborator,qualification):
    # numbered collaborator
    if data["qualifications"][qualification] in data["staff"][collaborator]["qualifications"]:
        return 1
    else:
        return 0

def project_necessary_qualifications(project,qualification):
    if data["qualifications"][qualification] in data["jobs"][project]["working_days_per_qualification"].keys():
        return data["jobs"][project]["working_days_per_qualification"][data["qualifications"][qualification]]
    else:
        return 0
def gain(project):
    return project["gain"]

def date_rendu(project):
    return project["due_date"]

def penalite(project):
    return project["daily_penalty"]



def solver_model(data,S,H,J,Q):
    #input : data , output : 
    # Create a new model
    m = Model()



    ## variables
    M = 1000
    ## Create variable rea (realisation of project)
    X = {}
    Y = {}
    L={}
    E= {}
    Debut = {}
    b = {}
    shift_change={}

    for i in range(S):
        for j in range(J):
            for k in range(Q):
                for t in range(H):
                    X[i,j,k,t] = m.addVar(vtype=GRB.BINARY,name="X["+str(i)+","+str(j)+","+str(k)+","+str(t)+"]")
    for j in range(J):
        Y[j]=m.addVar(vtype=GRB.BINARY,name="Y["+str(j)+"]")
        L[j]=m.addVar(vtype=GRB.INTEGER,name="L["+str(j)+"]")
        E[j]=m.addVar(vtype=GRB.INTEGER,name="E["+str(j)+"]")
        Debut[j]=m.addVar(vtype=GRB.INTEGER,name="Debut["+str(j)+"]")
    for i in range(S):
        for j in range(J):
            for k in range(Q):
                for t in range(H):
                    b[i,j,k,t] = m.addVar(vtype=GRB.BINARY,name="binary decision 2["+str(i)+","+str(j)+","+str(k)+","+str(t)+"]")
                    shift_change[i,j,k,t] = m.addVar(vtype=GRB.BINARY,name="Shift Change ["+str(i)+","+str(j)+","+str(k)+","+str(t)+"]")



    for i in range(S):
        for t in range(H):
            m.addConstr(quicksum(X[i,j,k,t] for j in range(J) for k in range(Q)) <=1)
    for i in range(S):
        for t in range(H):
            if vacations(data["staff"][i],t)>0:
                m.addConstr(quicksum(X[i,j,k,t] for j in range(J) for k in range(Q))==0)
    for i in range(S):
        for j in range(J):
            for k in range(Q):
                if (has_qualification(i,k)==0) or (project_necessary_qualifications(j,k)==0):
                    for t in range(H):
                        m.addConstr(X[i,j,k,t]==0)
    for j in range(J):
        for k in range(Q):
            if project_necessary_qualifications(j,k)>0:
                m.addConstr(Y[j]*project_necessary_qualifications(j,k) <= quicksum(X[i,j,k,t] for i in range(S) for t in range(H)))

    for j in range(J):
        for k in range(Q):
            if project_necessary_qualifications(j,k)>0:
                m.addConstr(quicksum(X[i,j,k,t] for i in range(S) for t in range(H)) <= project_necessary_qualifications(j,k))
            
    for i in range(S):
        for j in range(J):
            for k in range(Q):
                for t in range(H):
                    m.addConstr(X[i,j,k,t]*t <= E[j])
                    m.addConstr(t*X[i,j,k,t] >= Debut[j])
            m.addConstr(Debut[j] <= E[j])
                    
    for j in range(J):
        m.addConstr(E[j]-date_rendu(data["jobs"][j])<=L[j])




    ## Set objective function

    ## Fonction obj 1: Maximize profits
    profits = LinExpr()
    profits = quicksum( Y[j]*gain(data["jobs"][j]) - L[j]*penalite(data["jobs"][j]) for j in range(J))

    m.setObjective(profits,GRB.MAXIMIZE)

    #Update Modèle
    m.update()


    m.params.outputflag = 0

    solution_dict = {}
    for nbr_shifts in range(H,int(J/S),-1):
        for nbr_jours_max_projet in range(H,-1,-1):
            cons = []
            for i in range(S):
                for j in range(J):
                #for k in range(Q):
                    for t in range(H-1):                                
                        cons.append(m.addConstr(shift_change[i,j,k,t]>=0))
                        cons.append(m.addConstr(shift_change[i,j,k,t]>=quicksum(X[i,j,k,t+1]-X[i,j,k,t] for k in range(Q))))
                        cons.append(m.addConstr(shift_change[i,j,k,t]<=M*(1-b[i,j,k,t])))
                            #cons.append(m.addConstr(shift_change[i,j,k,t]<=X[i,j,k,t+1]-X[i,j,k,t]+M*b[i,j,k,t]))
                            #m.optimize()
                cons.append(m.addConstr(quicksum(shift_change[i,j,k,t] for j in range(J) for k in range(Q) for t in range(H)) <= nbr_shifts))
            cons.append(m.addConstr(E[j]-Debut[j] <= nbr_jours_max_projet))
            m.update()
            print("starting")
            m.optimize()
            solution_dict[nbr_shifts,nbr_jours_max_projet] = json.loads(m.getJSONSolution())
            print("nbr shifts",nbr_shifts,"nbr_jours_max_projet",nbr_jours_max_projet,solution_dict[nbr_shifts,nbr_jours_max_projet]["SolutionInfo"]["PoolObjVal"][0])

            for c in cons:
                m.remove(c)

    return solution_dict
    


# reduce format of gurobi output solution for some specific usages
def reduce_solution_format(solution_dict):
    solution_reduite = {}
    for key in solution_dict:
        solution_reduite[key[0],key[1],solution_dict[key]["SolutionInfo"]["ObjVal"]] = solution_dict[key]["Vars"]
    return solution_reduite

# select only non dominated solutions
def get_non_dominated_solutions(solution_reduite):
    # get the objective values
    obj_val = list(solution_reduite.keys())
    # get the number of solutions
    nb_sol = len(solution_reduite)
    # get the number of objectives
    nb_obj = 3
    # get the index of the solutions that are non dominated
    non_dominated_solutions = {}
    for i in range(nb_sol):
        dominated = False
        for j in range(nb_sol):
            if i != j:
                if all(obj_val[i][k] >= obj_val[j][k] for k in range(nb_obj-1)) and obj_val[i][nb_obj-1] <= obj_val[j][nb_obj-1]:
                    dominated = True
        if not dominated:
            non_dominated_solutions[obj_val[i]] = solution_reduite[obj_val[i]]
    return non_dominated_solutions
