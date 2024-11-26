def group_list(custom_list, size=4):
    final_list = []
    for i in range(0, len(custom_list), size):
        final_list.append(list(custom_list[i:i + size]))
    return final_list
