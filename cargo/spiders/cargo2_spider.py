import scrapy
import pickle
import time
import random
import re

class CargoSpider(scrapy.Spider):
    name = 'cargo2'
    start_urls = ['http://bietc.cgcworld.com']
    num_to_corp = dict()
    info_count = 0
    CONTENEUR_count = 0
    RORO_count = 0
    VRAC_count = 0
    info_total = 0

    account={ # use your own account
        '':{
            'user': '',
            'password': '',
        },
    }
    

    def __init__(self,date=None, *args, **kwargs):
        super(CargoSpider, self).__init__(*args, **kwargs)
        self.date = 'SearchDatedeb='+date[0:2]+'%2F'+date[2:4]+'%2F'+date[4:8]+'&SearchDatefin='+date[8:10]+'%2F'+date[10:12]+'%2F'+date[12:16]
        self.year = date[4:8]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata=self.account[''], # need to change to your account
            callback=self.after_login
        )
 
    def after_login(self, response):
        
        l = [
            'http://bietc.cgcworld.com/ListeBIC.asp?ACTION=SEARCH&numpage=' + str(num) + '&ListeStatut=2%7CA&SearchNum=&SearchManda= &' + self.date + '&SearchContnum=&SearchConttype=&SearchVractype=&SearchChassis=' \ # need to change
            for num in range(1,7)
        ]
        for url in l:
            yield scrapy.Request(url, callback=self.after_login2)

    
    def after_login2(self, response):
        num_l = list()
        corp_l = list()

        if len(response.css('tr[bgcolor] td[align=center] + td::text').extract()) < 3:
            # print('page ' + re.search(r'&numpage=(\d+)&', response.url).group(1) + ': No page')
            return

        for num in response.css('tr[bgcolor] td[align=center] + td::text').extract()[:15]:
            if num[7:14].isdigit():
                num_l.append(num[7:14])
        for corp in response.css("tr[bgcolor] td[colspan='6']::text").extract()[1::2]:
            corp_l.append(corp)
        
        print('processing page: ' + re.search(r'&numpage=(\d+)&', response.url).group(1))
        print(num_l)

        self.info_total = self.info_total + len(num_l)

        for i in range(len(num_l)):
            self.num_to_corp[num_l[i]] = corp_l[i]

        for a in response.css("tr[bgcolor] td[width='75'] a:nth-child(1)"):
            yield response.follow(a, callback=self.member_parse)    

        for num in num_l:
            yield scrapy.Request('http://bietc.cgcworld.com/marchandise.asp?I_TABLE=RORO&INITMARCH=Consulter&BIC_CLE=' + num[1:], callback=self.RORO)
            yield scrapy.Request('http://bietc.cgcworld.com/marchandise.asp?I_TABLE=CONTENEUR&INITMARCH=Consulter&BIC_CLE=' + num[1:], callback=self.CONTENEUR)
            yield scrapy.Request('http://bietc.cgcworld.com/marchandise.asp?I_TABLE=VRAC&INITMARCH=Consulter&BIC_CLE=' + num[1:], callback=self.VRAC)

    
    def RORO(self, response):
        # print('enter RORO')
        num = '0' + response.url[-6:]
        car = response.css('tr[valign=top] td:nth-child(2)::text').extract()
        print('yield: ' + num + ' RORO')
        self.RORO_count = self.RORO_count + 1
        print('info: ' + str(self.info_count) + '/%d' % self.info_total + ' | CONTENEYR: ' + str(self.CONTENEUR_count) + '/%d' % self.info_total + ' | VRAC: ' + str(self.VRAC_count) + '/%d' % self.info_total + ' | RORO: ' + str(self.RORO_count) + '/%d' % self.info_total)
        yield {
            'No': num,
            'Car': car,
        }

    def CONTENEUR(self, response):
        # print('enter CON')
        num = '0' + response.url[-6:]
        Type = response.css("tr[bgcolor='#ffffff'] td[width='35'] + td + td::text").extract()
        des = response.css("tr[valign=top] td[colspan='6'] div[style]::text").extract()
        print('yield: ' + num + ' CONTENEUR')
        self.CONTENEUR_count = self.CONTENEUR_count + 1
        print('info: ' + str(self.info_count) + '/%d' % self.info_total + ' | CONTENEYR: ' + str(self.CONTENEUR_count) + '/%d' % self.info_total + ' | VRAC: ' + str(self.VRAC_count) + '/%d' % self.info_total + ' | RORO: ' + str(self.RORO_count) + '/%d' % self.info_total)

        yield {
            'No': num,
            'Type': Type,
            'Des': des,
        }

    def VRAC(self, response):
        # print('enter VRAC')
        num = '0' + response.url[-6:]
        weight = response.css("tr[bgcolor='#ffffff'] td[width='35'] + td + td::text").extract_first()
        vol = response.css("tr[bgcolor='#ffffff'] td[width='35'] + td + td + td::text").extract_first()
        des = response.css("tr[bgcolor='#ffffff'] td[colspan='5'] div[style]::text").extract_first()
        print('yield: ' + num + ' VRAC')
        self.VRAC_count = self.VRAC_count + 1
        print('info: ' + str(self.info_count) + '/%d' % self.info_total + ' | CONTENEYR: ' + str(self.CONTENEUR_count) + '/%d' % self.info_total + ' | VRAC: ' + str(self.VRAC_count) + '/%d' % self.info_total + ' | RORO: ' + str(self.RORO_count) + '/%d' % self.info_total)
        yield {
            'No': num,
            'Weight': weight,
            'Vol': vol,
            'Des': des,
        }

    def member_parse(self, response):
        num = response.css('h5::text').extract_first()[3:]
        i = response.css("tr tr tr:nth-child(2) span.InputVisu::text").extract()

        print('yield: ' + num + ' info')
        self.info_count = self.info_count + 1
        print('info: ' + str(self.info_count) + '/%d' % self.info_total + ' | CONTENEYR: ' + str(self.CONTENEUR_count) + '/%d' % self.info_total + ' | VRAC: ' + str(self.VRAC_count) + '/%d' % self.info_total + ' | RORO: ' + str(self.RORO_count) + '/%d' % self.info_total)     
        yield {
            'No': num,
            'Corp': self.num_to_corp[num],
            'Shipper_Name': i[0],
            'Shipper_Address': i[1],
            'Shipper_Address2': i[2],
            'Shipper_ZIP_Code': i[3],
            'Shipper_City_State': i[4],
            'Shipper_Country': i[5],
            'Shipper_Phone': i[6],
            'Shipper_Email': i[7],
            'Consignee_Name': i[8],
            'Consignee_Address': i[9],
            'Consignee_Address2': i[10],
            'Consignee_ZIP_Code': i[11],
            'Consignee_City_State': i[12],
            'Consignee_Country': i[13],
            'Consignee_Phone': i[14],
            'Consignee_Email': i[15],
            'Year': self.year,
            'Goods_Value': i[-10],
        }
        
        


        
