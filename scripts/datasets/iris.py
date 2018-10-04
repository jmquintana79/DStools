# -*- coding: utf-8 -*-
# @Author: Juan Quintana
# @Date:   2018-09-18 09:24:26
# @Last Modified by:   Juan Quintana
# @Last Modified time: 2018-10-04 15:42:04


"""
DATASET Scikit-Learn Iris.
"""
import numpy as np
from pandas import DataFrame
import sys
sys.path.append('../')
from tools.reader import columns
from sklearn.datasets import load_iris
import click


def load()->tuple:
    """
    Load Scikit-Learn Iris dataset.
    return -- tuple(dataframe data, dictionary columns)
    """
    # header
    click.secho('Load data..', fg='green')
    # get dataset
    iris = load_iris()
    # store into dataframe
    df = DataFrame(np.c_[iris.data, iris.target], columns=list(iris.feature_names)+['y'])
    # format
    df.y = df.y.astype('category')
    # get dcol
    col = columns()
    col.get(df, ['y'])
    # return
    return (df, col)


def save(path: str):
    """
    Save Scikit-Learn dataset.
    """
    # load dataset
    data, dcol = load()
    # store into a csv file
    try:
        data.to_csv(path, index=False)
        # screen
        click.secho('It was saved "%s" successfully.' % click.format_filename(path, shorten=True), fg='green')
    except Exception as e:
        click.secho('It could not be saved "%s" successfully.' % click.format_filename(path, shorten=True), fg='red')
        click.echo(str(e))

    # return
    return None


if __name__ == '__main__':
    # load data
    data, col = load()
    print(col.all)
    # save data
    # save('dataset.iris.csv')
