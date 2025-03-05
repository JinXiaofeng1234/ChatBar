
def index_check(index):
    special_index_ls = [0, 4, 7]
    if index in special_index_ls:
        return index
    else:
        return index - 1

