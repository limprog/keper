
def read():
    with open('config.txt', 'r') as f:
        tgid = f.readline()
        timetabel = f.readline()
        id = f.readline()
        date_of_week = f.readline()
        time = f.readline()
        f.close()
    return tgid, timetabel, id, date_of_week, time


def write(data):
    with open('config.txt', "w") as f:
        date_of_week = data['timetabel'][:3]
        time = data['timetabel'][4:]
        f.write(f'{data["tgid"]}\n{data["timetabel"]}\n{data["id"]}\n{date_of_week}\n{time}')
        f.close()