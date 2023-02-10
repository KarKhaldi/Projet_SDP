import skcriteria as skc
from skcriteria.madm import similarity  # here lives TOPSIS
from skcriteria.pipeline import mkpipe  # this function is for create pipelines
from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.madm import simple
from skcriteria.madm import electre
from skcriteria.cmp import RanksComparator, mkrank_cmp

from skcriteria.pipeline import mkpipe
from skcriteria.preprocessing.invert_objectives import (
    InvertMinimize,
    NegateMinimize,
)
from skcriteria.preprocessing.filters import FilterNonDominated
from skcriteria.preprocessing.scalers import SumScaler, VectorScaler
from skcriteria.madm.simple import  WeightedSumModel
from skcriteria.madm.similarity import TOPSIS
import pandas as pd


def main_fuction(non_dominated_sol):
    dataframe_solutions = pd.DataFrame(columns=["NBR_SHIFTS","MAX_DAYS_PER_PROJEJT","GAIN"])
    for i,j,k in non_dominated_sol.keys():
        dataframe_solutions = dataframe_solutions.append(pd.DataFrame([[i,j,k]],
                                                                    columns = ["NBR_SHIFTS","MAX_DAYS_PER_PROJEJT","GAIN"]))
    dataframe_solutions = dataframe_solutions.reset_index(drop=True)

    matrix = dataframe_solutions.values



    dm = skc.mkdm(
        matrix,
        [min, min, max],
        weights=[0.02, 0.03, 0.95],
        criteria=["nbr shifts", "max days", "gain"],
    )
    ws_pipe = mkpipe(
        InvertMinimize(),
        FilterNonDominated(),
        SumScaler(target="weights"),
        VectorScaler(target="matrix"),
        WeightedSumModel(),
    )


    tp_pipe = mkpipe(
        NegateMinimize(),
        FilterNonDominated(),
        SumScaler(target="weights"),
        VectorScaler(target="matrix"),
        TOPSIS(),
    )



    wsum_result = ws_pipe.evaluate(dm)
    tp_result = tp_pipe.evaluate(dm)

    display(wsum_result, tp_result)

    RanksComparator([("ts", tp_result), ("ws", wsum_result)])
    rcmp = mkrank_cmp(tp_result, wsum_result)



    rcmp.to_dataframe()


    fig, axs = plt.subplots(1, 1, figsize=(10, 10))
    rcmp.plot.flow()
    plt.show()


    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 2, figsize=(20, 5))

    rcmp.plot.bar(ax=axs[0])
    rcmp.plot.barh(ax=axs[1])

    fig.tight_layout();



    fig, axs = plt.subplots(1, 2, figsize=(20, 5))

    rcmp.plot.box(ax=axs[0])
    rcmp.plot.box(ax=axs[1], orient="h")

    fig.tight_layout();