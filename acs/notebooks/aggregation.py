from utils import get_adjusted_year
from math import prod

# weighted sum
def weighted_sum(values, percents):
    return sum([value * percent for value, percent in zip(values, percents)])

# weighted arithmetic mean
def weighted_amean(values, pops):
    return sum([value * pop for value, pop in zip(values, pops)]) / sum(pops)

def weighted_gmean(values, pops):
    # normalize pops
    norm = sum(pops)
    pops = [pop / norm for pop in pops]
    # calculate the geometric mean weighted by adjusted_pops
    return prod([value ** pop for value, pop in zip(values, pops)]) ** (1 / sum(pops))

def aggregate_statistic(agg_type, values, pops):
    if agg_type == 'mean':
        return weighted_amean(values, pops)
    elif agg_type in ['percentage', 'ratio']:
        return weighted_amean(values / 100, pops) * 100
    elif agg_type == 'median':
        return weighted_gmean(values, pops)
    else:
        print(f'Unrecognized type: {agg_type}')

def names_to_labels(selected_variables, dataframe):
    df = dataframe.copy()
    for sv_index, sv_row in selected_variables.iterrows():
        label = sv_row['2022_label']
        data = []
        for acs_index, acs_row in df.iterrows():
            year = get_adjusted_year(acs_row['year'])
            var_name = sv_row[f'{year}_name']
            if '***' in var_name:
                var_name = var_name.split('***')
                total = 1
                for var in var_name:
                    total *= float(acs_row[var])
                    if var.endswith('PE'):
                        total /= 100.0
                data.append(total)
            else:
                data.append(acs_row[var_name])
        df[label] = data

    # drop all columns where the name starts with DP
    new_columns = [col for col in df.columns if not col.startswith('DP')]
    df = df[new_columns]
    return df