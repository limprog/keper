import requests
import argparse
from txt_reader import *
url = 'http://127.0.0.1:5000'


def reg():
    print("Для регистрации ведите свой никнем")
    nickname = input()
    print("ведите номер кабинета")
    socet = input()
    print("введите название организации")
    op = input()
    data = {}
    data['nickname'] = nickname
    data['socet'] = socet
    data['op'] = op
    r = requests.post(url+'/comp/reg', data=data)
    if r.status_code == 201:
        data2 = r.json()
        write(data2)
        print("все хорошо")
    else:
        print("повторите регистрацию")
        reg()




if __name__ == '__main__':
    reg()