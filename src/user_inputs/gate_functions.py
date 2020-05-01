#
#   user_inputs script with gate functions
#   Prepared by user - should match the data
# ---------------------------------------- #


def bin_and(data):

    if data[0] == 1 and data[1] == 1:
        return 1
    else:
        return 0


def bin_or(data):

    if data[0] == 0 and data[1] == 0:
        return 0
    else:
        return 1


def bin_xor(data):

    if data[0] == data[1]:
        return 0
    else:
        return 1


def bin_nand(data):

    if data[0] == 1 and data[1] == 1:
        return 0
    else:
        return 1
