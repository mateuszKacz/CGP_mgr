#
#   user_inputs script with objective function
#   Prepared by user - should match the data
# ---------------------------------------- #


def obj_func(data_input, net_output):
    """Sample user-defined function"""
    score = []
    for i in range(len(data_input)):
        if data_input[i][5] == net_output[i]:
            score.append(0)
        else:
            score.append(1)

    return sum(score)/len(net_output)
