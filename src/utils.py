# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta

import pandas as pd

from .config import (
    URL,
    REQUEST_PARAMS,
    STATIONS_SCHEMA,
    ERROR_CODE_SCHEMA
)


_PROJ_PATH = os.path.dirname(__file__)


def load_stations(replace_schema=True):
    """load_stations

    Parameters
    ----------

    replace_schema : bool

    Returns
    -------
    stations : pd.DataFrame
    """

    data_path = os.path.join(_PROJ_PATH, 'metadata', 'stations.csv')
    stations = pd.read_csv(data_path)

    if replace_schema:
        stations.columns = STATIONS_SCHEMA

    return stations


def load_error_code(replace_schema=True):
    """load_error_code

    Parameters
    ----------

    replace_schema : bool

    Returns
    -------
    error_code : pd.DataFrame
    """

    data_path = os.path.join(_PROJ_PATH, 'metadata', 'error_code.csv')
    error_code = pd.read_csv(data_path)

    if replace_schema:
        error_code.columns = ERROR_CODE_SCHEMA

    return error_code


def get_base_url(service_key_path):
    """get_base_url

    Parameters
    ----------

    service_key_path : str

    Returns
    -------
    url : str
        - base url formmated with service key
    """

    with open(service_key_path, 'r') as f:
        service_key = f.read()
        if service_key.endswith('\n'):
            service_key = service_key[:-1]

    url = URL.format(service_key=service_key)

    return url


def create_date_sequence(start_date, end_date, interval):
    """create_date_sequence

    Parameters
    ----------

    start_date : str
        - yyyy-mm-dd
    end_date : str
        - yyyy-mm-dd
    interval : int

    Returns
    -------
    date_seq : list
        - [start_date,
           start_date + interval*1,
           start_date + interval*2,
           ...,
           end_date]
    """

    # maximum rows per request should be less then 1000
    interval = 40

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    n_days = (end_date - start_date).days

    # iterate over this date list
    date_seq = [
        start_date + timedelta(days=d)
        for d in range(n_days+1)
    ]
    date_seq = date_seq[::(interval)]
    if date_seq[-1] != end_date:
        date_seq += [end_date]

    return date_seq


def update_params(**kwargs):
    """update_params

    Parameters
    ----------

    **kwargs : dict
        - see config.py for available keys

    Returns
    -------
    """

    params = {k: v for k, v in REQUEST_PARAMS.items()}
    for k, v in kwargs.items():
        params[k] = v

    return params


if __name__ == '__main__':
    stations = load_stations(True)
    error_code = load_error_code(True)
    print(stations.head())
    print(error_code.head())
