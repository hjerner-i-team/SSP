def pre_process_rows(data):
    avg = sum(data) / len(data)
    return avg

def pre_process_segments(data):
    avg = [sum(x) / len(x) for x in data]
    return avg

