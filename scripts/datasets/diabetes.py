# -*- coding: utf-8 -*-
# @Author: Juan Quintana
# @Date:   2018-09-18 09:24:26
# @Last Modified by:   Juan Quintana
# @Last Modified time: 2018-09-18 10:20:28


"""
DATASET Scikit-Learn.
"""
import numpy as np
from pandas import DataFrame
import sys
sys.path.append('../scripts/')
from tools.reader import get_dcol
from sklearn.datasets import load_diabetes
import click


def load()->tuple:
    """
    Load Scikit-Learn dataset.
    return -- tuple(dataframe data, dictionary columns)
    """
    # header
    click.secho('Load data..', fg='green')
    # get dataset
    diabetes = load_diabetes()
    # store into dataframe
    df = DataFrame(np.c_[diabetes.data, diabetes.target], columns=list(diabetes.feature_names)+['y'])
    # get dcol
    dcol = get_dcol(df, ltarget=['y'])
    # return
    return (df, dcol)


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
    #data, dcol = load()
    # save data
    save('dataset.diabetes.csv')
