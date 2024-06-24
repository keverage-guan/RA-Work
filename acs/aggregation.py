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
