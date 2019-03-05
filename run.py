import subprocess
import time

account_name = 'HK'

date_list = [
    '0105201501062015',
    '0206201501072015',
    '0207201501082015',
    '0208201501092015',
    '0209201501102015',
    '0210201501112015',
    '0211201501122015',
    '0212201501012016',
    '0201201601022016',
    '0202201601032016',
    '0203201601042016',
    '0204201601052016',
    '0205201601062016',
    '0206201601072016',
    '0207201601082016',
    '0208201601092016',
    '0209201601102016',
    '0210201601112016',
    '0211201601122016',
    '0212201601012017',#
    '0201201701022017',
    '0202201701032017',
    '0203201701042017',
    '0204201701052017',
    '0205201701062017',
    '0206201701072017',
    '0207201701082017',
    '0208201701092017',
    '0209201701102017',
    '0210201701112017',
    '0211201701122017',
    '0212201701012018',#
    '0201201801022018',
    '0202201801032018',
    '0203201801042018',
    '0204201801052018',
    '0205201801062018',
    '0206201801072018',
    '0207201801082018',
    '0208201801092018',
    '0209201801102018',
    '0210201801112018',
    '0211201801122018',
    '0212201831122018',
]

def main():
    for date in date_list:
        print(
            """

            ------------ %s from %s/%s/%s to %s/%s/%s ------------
            
            """ % (account_name,date[0:2],date[2:4],date[4:8],date[8:10],date[10:12],date[12:16])
            )
        try:
            subprocess.run('scrapy crawl cargo2 -a date=%s -o ./out/%s.json -s LOG_FILE=./out/%s.log' % (date,account_name+date, account_name+date), shell=True).check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)
            return
        print(
            """

            ------------  %s from %s/%s/%s to %s/%s/%s compeleted, wait 1 mins------------
            
            """ % (account_name,date[0:2],date[2:4],date[4:8],date[8:10],date[10:12],date[12:16])
            )
        time.sleep(60)

if __name__ == '__main__':
    main()