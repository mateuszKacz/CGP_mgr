#
#   user_inputs script with objective function
#   Prepared by user - should match the data
# ---------------------------------------- #


def obj_func(data_input, net_output):
    """Sample user-defined function"""
    score = []
    for i in range(len(data_input)):
        score.append(abs(data_input[i][5] - net_output[i]))

    return sum(score)
