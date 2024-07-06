# Import modules
import regex as re
import requests
import json

def query(year, selected_variables, for_param, key):
    adjusted_year = get_adjusted_year(year)
    data_dict = {}
    for query_year in range(adjusted_year, adjusted_year - 3, -1):
        try: 
            variables = ','.join(list(selected_variables[f'{query_year}_name'])).replace('***', ',')

            url = f"https://api.census.gov/data/{query_year}/acs/acs5/profile?get={variables}&for={for_param}&key={key}"

            response = requests.get(url)
            data = json.loads(response.text)
            # append each array of data to each array of all_data
            for i in range(len(data[0])):
                data_dict[data[0][i]] = data[1][i]
            break
                    
        except Exception as e:
            if query_year == adjusted_year -3:
                print(f"Error: {e}")
                exit()
            else:
                continue
    return data_dict

def get_place_for_param(geocode_row):
    state_code = str(geocode_row['State Code (FIPS)'].values[0]).zfill(2)
    geo_type = geocode_row['geo_type'].values[0]

    if geo_type == 'state':
        return f'state:{state_code}'
    elif geo_type == 'county':
        county_code = str(int(geocode_row['County Code (FIPS)'].values[0])).zfill(3)
        return f'county:{county_code}&in=state:{state_code}'
    elif geo_type in ['city', 'town']:
        place_code = str(int(geocode_row['Place Code (FIPS)'].values[0])).zfill(5)
        return f'place:{place_code}&in=state:{state_code}'
    
def get_adjusted_year(year):
    if year <= 2006:
        return 2009
    elif year >= 2021:
        return 2022
    else:
        return year + 2