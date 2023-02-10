import plotly.graph_objects as go
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


## must refactor size 
def plotting_figure(non_dominated_sol,solution_dict):


    Z = np.zeros((24,24))

    for i in range(24):
        for j in range(24):
            try:
                Z[j,i]=solution_dict[i,j]["SolutionInfo"]["PoolObjVal"][0]
                print(i,j,solution_dict[i,j]["SolutionInfo"]["PoolObjVal"][0])
            except:
                Z[i,j]=0
                continue

    fig = go.Figure(go.Surface(
        
        contours = {
            "z": {"show": True, "start": 0, "end":np.max(Z) , "size": 1, "color":"black"}
        },
        x = np.arange(24),
        y = np.arange(24),
        z = Z,
        colorscale = 'RdBu',
        showscale = True
    ))

    for key in non_dominated_sol.keys():
        print(key)
        fig.add_scatter3d(x=[key[0]], y=[key[1]], z=[key[2]], mode='markers', marker=dict(size=10, color='red'), showlegend=False)




    fig.update_layout(
            scene = {
                "xaxis": {"nticks": 0},
                "zaxis": {"nticks": 0},
                'camera_eye': {"x": 1, "y": 1, "z": 1},
                "aspectratio": {"x": 0, "y": 0, "z": 1}
            } ,
            margin=go.layout.Margin(
            l=0, 
            r=0, 
            b=0, 
            t=0, 
        )
            ) 

    fig.update_layout(scene = dict(
                        xaxis_title='Shifts',
                        yaxis_title='Jours',
                        zaxis_title='Gain'),
    )

            
    fig.show()
    return fig