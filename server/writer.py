import os
from datetime import  datetime, date
os.makedirs('loogs', exist_ok=True)


def writer(id, result):
    today = str(date.today())
    os.makedirs(f'loogs/{today}', exist_ok=True)
    if os.path.isfile(f'loogs/{today}/{id}.csv'):
        with open(f'loogs/{today}/{id}.csv', "a") as f:
            now = datetime.now()
            now_time = now.strftime("%H_%M_%S")
            f.write(f"\n{now_time},{result['pred_class']}")
            f.close()
    else:
        with open(f'loogs/{today}/{id}.csv', "w") as f:
            f.write(f"time,result")
            now = datetime.now()
            now_time = now.strftime("%H_%M_%S")
            f.write(f"\n{now_time},{result['pred_class']}")
            f.close()



