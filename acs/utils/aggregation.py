import pandas as pd

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
    return sum([value ** pop for value, pop in zip(values, pops)]) ** (1 / sum(pops))

def aggregate_statistic(agg_type, values, pops):
    if agg_type == 'mean':
        return weighted_amean(values, pops)
    elif agg_type in ['percentage', 'ratio']:
        return weighted_amean(values / 100, pops) * 100
    elif agg_type == 'median':
        return weighted_gmean(values, pops)
    else:
        print(f'Unrecognized type: {agg_type}')