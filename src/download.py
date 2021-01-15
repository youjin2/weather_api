# -*- coding: utf-8 -*-

import time
import os
import json
import argparse

import pandas as pd
import requests

from .utils import (
    get_base_url,
    update_params,
    create_date_sequence,
    load_stations,
)


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--kpath', dest='key_path', type=str)
    parser.add_argument('--dpath', dest='download_path', type=str)
    parser.add_argument('--sdate', dest='start_date', type=str,
                        help='yyyy-mm-dd')
    parser.add_argument('--edate', dest='end_date', type=str,
                        help='yyyy-mm-dd')
    parser.add_argument('--interval', dest='interval', type=int,
                        default=40)

    return parser.parse_args()


def main():

    parsed = parse_args()

    # get base url
    base_url = get_base_url(parsed.key_path)
    # data will be saved to this path
    os.makedirs(parsed.download_path, exist_ok=True)

    # start, end date lists to reqeust
    date_list = create_date_sequence(parsed.start_date,
                                     parsed.end_date,
                                     parsed.interval)

    # iterate over station locations
    stations = load_stations()
    stations['start_date'] = pd.to_datetime(stations.start_date,
                                            format='%Y-%m-%d')
    stations['end_date'] = pd.to_datetime(stations.end_date,
                                          format='%Y-%m-%d')
    stations = stations[stations.end_date.isnull() |
                        (stations.end_date.dt.date > date_list[-1])]
    stn_ids = sorted(stations.stn_id.tolist())

    # append failure request logs to this data
    log_columns = ['result_code', 'error_message', 'params']
    log_data = pd.DataFrame(columns=log_columns)

    # start downloading data
    start_time = time.time()
    for stn_id in stn_ids:
        file_name = os.path.join(parsed.download_path,
                                 'stn_{}.csv'.format(stn_id))
        weather_data = pd.DataFrame()

        print('====='*5)
        print('stn_id: {}'.format(stn_id))
        print('====='*5)

        for i in range(len(date_list)-1):
            start, end = date_list[i], date_list[i+1]
            num_days = (end - start).days

            # update request params for each iteration
            param_dict = {
                'numOfRows': (num_days+1)*24,
                'startDt': start.strftime('%Y%m%d'),
                'endDt': end.strftime('%Y%m%d'),
                'stnIds': stn_id,
            }
            cur_params = update_params(**param_dict)
            try:
                result = requests.get(base_url, params=cur_params)
                response = json.loads(result.text)['response']
                # result_cd = response.get('header').get('resultCode')
                data_list = response.get('body').get('items').get('item')
            except Exception as ex:
                result_cd = '999'
                error_log = [result_cd, str(ex), cur_params]
                log_data = log_data.append(
                    pd.DataFrame([error_log], columns=log_columns))
            else:
                weather_data = weather_data.append(pd.DataFrame(data_list))
            finally:
                print('time elapsed: {} sec ({}~{})'.
                      format(time.time() - start_time, start, end))

        weather_data.to_csv(file_name, index=False)


if __name__ == '__main__':
    main()
