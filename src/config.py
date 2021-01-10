# -*- coding: utf-8 -*-

# pass personal service key
URL = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList' +\
    '?serviceKey={service_key}'


# fill below Nones
REQUEST_PARAMS = {
    'pageNo': 1,
    # 24 * days (< 1000 is required)
    'numOfRows': None,
    'dataType': 'JSON',
    'dataCd': 'ASOS',
    'dateCd': 'HR',
    # yyyymmdd in str format
    'startDt': None,
    # yyyymmdd in str format
    'endDt': None,
    'startHh': '00',
    'endHh': '23',
    # station id in str format
    'stnIds': None
}


STATIONS_SCHEMA = [
    'stn_id',
    'start_date',
    'end_date',
    'stn_name',
    'stn_address',
    'department',
    'latitude',
    'longitude',
    'altitude',
    'pressure_height',
    'temperature_height',
    'wind_speed_height',
    'precipitation_height',
]


ERROR_CODE_SCHEMA = [
    'error_code',
    'error_message',
    'description',
]
