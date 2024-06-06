def validate(policy, proposal, risky, keywords):
    # check that policy is either 0 or 1
    if policy not in [0, 1]:
        return False
    # if policy is 0, proposal, risky, and keywords should be nan
    if policy == 0 and (proposal or risky):
        return False
    # if policy is 1, proposal and risky should be 0 or 1
    if policy == 1 and (proposal > 1 or proposal < 0 or risky not in [0, 1]):
        return False
    return True