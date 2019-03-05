import demjson
from tqdm import tqdm

account = ''

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
    with open('./out/out_%s.json' % account, 'w') as out:
        file_name_list = [('./out/' + account + x + '.json') for x in date_list]
        out_json = list()
        for file_name in tqdm(file_name_list):
            with open(file_name, 'r') as f:
                json = demjson.decode(f.read())
                for info in [x for x in json if 'Corp' in x]:
                    for item in info.items():
                        info[item[0]] = item[1].replace('\xa0',' ').strip()
                    info['Freight'] = list()
                    info['Bulk'] = dict()
                    info['Vehicles'] = list()
                    for att in [x for x in json if (x['No']==info['No']) and ('Corp' not in x)]:
                        if 'Type' in att:
                            for i in range(len(att['Type'])):
                                info['Freight'].append({
                                    'Type': att['Type'][i].replace('\xa0',' ').strip(),
                                    'Description': att['Des'][i] and att['Des'][i].replace('\xa0',' ').strip() or '',
                                })
                        if 'Car' in att:
                            for i in range(len(att['Car'])):
                                info['Vehicles'].append({
                                    'Brand': att['Car'][i].replace('\xa0',' ').strip(),
                                })
                        
                        if 'Weight' in att and att['Weight'] is not None:
                            info['Bulk'] = {
                                'Weight': att['Weight'].replace('\xa0',' ').strip(),
                                'Vol': att['Vol'] and att['Vol'].replace('\xa0',' ').strip() or '',
                                'Description': att['Des'] and att['Des'].replace('\xa0',' ').strip() or '',
                            }
                        
                    out_json.append(info)
                f.close()
        out.write(demjson.encode(out_json))
        out.close()

                    
                            
                            



if __name__ == '__main__':
    main()
