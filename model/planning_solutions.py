
import numpy as np
import pandas as pd



def listing_solutions(non_dominated_sol):
    list_solution = []
    for key, value in non_dominated_sol.items():
        solution = {}
        for i in range(len(value)):
            if value[i]['VarName'][:2]=="X[":
                index = value[i]['VarName']
                index_to_vec = index.split("[")[1].split("]")[0].split(",")
                index_to_vec = [int(i) for i in index_to_vec]
                solution[index_to_vec[0],index_to_vec[1],index_to_vec[2],index_to_vec[3]] = value[i]['X']

        list_solution.append(solution)
    return list_solution



def get_planning(solution,data,S,J,Q,H):
    # Dataframe with affectations
    planning = pd.DataFrame(np.nan, columns = ["day_"+str(i) for i in range(H)],index = [i for i in range(S)])
    for i in range(S): # I
        for j in range(J): # P
            for k in range(Q): # Q
                for t in range(H): # J
                    if (i,j,k,t) in solution:
                        planning.iloc[i,t] = k
    ## colors cells with regard to project
    color_pro = {}
    for i in range(J):
        color_pro[i] = '#%06X' % np.random.randint(0, 0xFFFFFF)

    df_color = pd.DataFrame(np.nan, columns = ["day_"+str(i) for i in range(H)],index = [i for i in range(S)])
    for i in range(S): 
        for j in range(J): 
            for k in range(Q):
                for t in range(H): 
                    if (i,j,k,t) in solution: 
                            df_color.iloc[i,t] = color_pro[j]
    df_color = df_color.applymap(lambda x: 'background-color: {}'.format(x))
    def highlight_1(x):
        return pd.DataFrame(df_color.values, columns=x.columns)
    planning = planning.astype('Int64')
    planning = planning.style.apply(highlight_1,axis=None)
    # Mapping colors to projects
    proj_col = pd.DataFrame()
    i=0
    jobs = [ job["name"] for job in data['jobs']]
    for project in jobs:
        proj_col = pd.concat([proj_col,pd.DataFrame({'project':project,'color': 'background-color: ' + color_pro[i]},index=[i])], axis=0)
        i+=1
    def highlight_2(x):
        return x
    proj_col = proj_col.style.apply(highlight_2,axis=None, subset=['color'])
    return planning, proj_col