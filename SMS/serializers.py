from rest_framework import serializers
from .models import Clients,Templates,Messages,Admin
import re
from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher
from collections import defaultdict, OrderedDict
#import dryscrape
import os, sys, logging, linecache

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	msg = ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
	print msg

def extract(vendor, product_name) :
    d = defaultdict(list)
    di = OrderedDict()
    if vendor == "amazon" : 
        product = product_name.replace(" ", "+")
        product.lower()
        url1 = 'http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + product
        response = requests.get(url1, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content)
        rs = ['result_0', 'result_1', 'result_2', 'result_3', 'result_5','result_6']
        
        i = 0
        for res in rs :
            bs = soup.find('li', attrs = {'id' : res } )
            name = bs.find('h2')
            name = name.text
	    if name.find(product_name) == -1:
	        continue
        
            key = str(i)
            d[key].append(name)
        
            try :
                rate  = bs.find('span', attrs = { 'class' : 'a-color-price'})
                rate = rate.text.strip()
            except AttributeError : 
                rate = 0
        
            d[key].append(rate)
        
            try :
                rating = bs.find('span', attrs = { 'class' : 'a-declarative'})
                rat = rating.text
                r = re.findall("\d+[\.]?\d*", rat)
            except AttributeError :
                r = [0, 0]
            d[key].append(float(r[0]))
            i = i + 1
    elif vendor == "snapdeal" :
        product = product_name.replace(" ", "%20")
        product = product.lower()
        url1 = "https://www.snapdeal.com/search?keyword=" + product + "&santizedKeyword=&catId=&categoryId=0&suggested=false&vertical=&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy"
        response = requests.get(url1, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content)

        rs = ['0', '1', '2', '3']
        i = 0
        
        for res in rs :
            bs = soup.find('div', attrs = {'data-js-pos' : res } )

            try :
                name = bs.find('p', attrs = {'class' : 'product-title'})
            except :
                time.sleep(10)
                response = requests.get(url1, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
                soup = BeautifulSoup(response.content)
                bs = soup.find('div', attrs = {'data-js-pos' : res } )
                name = bs.find('p', attrs = {'class' : 'product-title'})
            name = name.text
        
            key = str(i)
            d[key].append(name)

            try :
                rate  = bs.find('span', attrs = { 'class' : 'lfloat product-price'})
                rate = rate.text.strip()
            except AttributeError : 
                rate = 0
        
            d[key].append(rate)
        
            try :
                rating = bs.find('div',style = True )
                rat = rating['style']
                r = re.findall("\d+[\.]?\d*", rat)
                ratin = (float(r[0])/100)*5
            except TypeError :
                ratin = 0
        
            d[key].append(ratin)
            i = i+1
    elif vendor == "koovs" :
        product = product_name.replace(" ", "-")
        product = product.lower()
        url1 = "http://www.koovs.com/" + product
        response = requests.get(url1, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content)

        rs = ['1', '2', '3', '4']
        i = 0
        
        for res in rs :
            bs = soup.find('div', attrs = {'unbxdparam_prank' : res } )
            key = str(i)
            name = bs.find('div', attrs = {'class' : "prodDescp"})
            name = name.text.strip()
            n = re.match( r'(\w+\s)+', name)
            name = n.group()
            d[key].append(name.strip())

            try :
                rate  = bs.find('span', attrs = { 'class' : 'prodPrice'})
                rate = rate.text.strip()
            except AttributeError : 
                rate = 0
            d[key].append(rate)
    
            ratin = 0
            d[key].append(ratin)
            i = i+1     
    elif vendor == "myntra" :
        product = product_name.replace(" ", "-")
        product = product.lower()
        url1 = "http://www.myntra.com/" + product + "?userQuery=true"
        response = requests.get(url1, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'html.parser')
        bs = soup.findAll("script") #, attrs = { 'type' : 'text/javascript'})
        data = bs[6]
	#print "data", data
        price = re.findall(r'\"discounted_price\"\:\d+', str(data))
        name = re.findall(r'\"stylename\"\:\"[a-zA-Z0-9\- ]+', str(data))
	if name:
            for x in range(len(name)):
                key = str(x)
                name[x] = name[x].split(":")
                n = name[x][1].strip("\"")
                d[key].append(n)
                price[x] = price[x].split(":")
                p = int(price[x][1])
                d[key].append(p)
                r = 0
                d[key].append(float(r))
    elif vendor == 'flipkart' :
        product = product_name.replace(" ", "%20")
        product = product.lower()
        url = "https://www.flipkart.com/search?q=" + product_name + "&otracker=start&as-show=on&as=off"
	sess = None
	"""
	try:
       		#sess = dryscrape.Session(url)
       		sess = dryscrape.Session()
		print dir(sess)
		print '--------------------------------------------------------------------------'
	except Exception as e:
		import os,sys,linecache
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		linecache.checkcache(filename)
		line = linecache.getline(filename, lineno, f.f_globals)
		msg = ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
		print(msg)
	"""
	sess = None#dryscrape.Session()
        sess.visit(url)
        response = sess.body()
        soup = BeautifulSoup(response)
        bs = soup.findAll("div" , attrs = { 'class' : 'col col-3-12 col-md-3-12 MP_3W3'})
        x = 0
        if len(bs) == 0 :
            bs = soup.findAll("div" , attrs = { 'class' : 'col _2-gKeQ'})
            for i in bs :
                key = str(x)
                try :
                    title = i.find("div", attrs = { 'class' : '_3wU53n'})
                    name = title.text
                except AttributeError :
                    name = "None"
                d[key].append(name) 

                try :
                    price = i.find("div", attrs = { 'class' : '_1vC4OE _2rQ-NK'})
                    price = price.text
                    price = re.findall(r'\d+\.?\d*', str(price))
                    p = price[0]
                except AttributeError :
                    p = 0
                d[key].append(float(p))
                try :
                    rating = i.find("div", attrs = { 'class' : 'hGSR34 _2beYZw'})
                    rating = rating.text
                    rate = re.findall(r'\d+\.?\d*', str(rating))
                    r = rate[0]
                except AttributeError :
                    r = 0
                d[key].append(float(r))
                x = x+1  
        else :
            for i in bs:
                key = str(x)
                try :
                    name = i.find("a", attrs = { 'class' : '_2cLu-l'})
                    name = name.text
                except AttributeError :
                    name = 'None'

                d[key].append(name)
                try :
                    price = i.find("div", attrs = {"class" : "_1vC4OE"})
                    price = price.text
            
                    price = re.findall(r'\d+\.?\d*', str(price))
                    p = price[0]
                except AttributeError :
                    price = 0

                d[key].append(float(p))
                try :
                    rating = i.find("div", attrs = {'class' : 'hGSR34 _2beYZw'})
                    rating = rating.text
                    rate = re.findall(r'\d+\.?\d*', str(rating))
                    r = rate[0]
                except AttributeError :
                    r = 0
                d[key].append(float(r))
                x = x+1
    elif vendor == 'paytm':
        product = product_name.replace(" ", "%20")
        product = product.lower()

        url = "https://paytm.com/shop/search?q=" + product + "&from=organic&child_site_id=1&site_id=1"
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content)
        bs = soup.find('div', attrs = {'class' : '_1fje'})
        try :
            name = bs.findAll('div', attrs = {'class' : '_2apC'})
            price = bs.findAll('span', attrs = {'class' : '_1kMS'})
            for i in range(4) :
                key = str(i)
                d[key].append(name[i].text)
                p = price[i].text
                p = re.findall(r'\d+\.?\d*', str(p))
                pr = p[0]
                d[key].append(float(pr))
                rating = 0
                d[key].append(rating)

        except : 
            for i in range(4) :
                key = str(i)
                d[key].append('None')
                d[key].append(0)
                rating = 0
                d[key].append(rating)

    di = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
    k = -1
    similarity = []
   
    if di:
        for x in di :
            sim = SequenceMatcher(None, product_name.lower(), di[x][0].lower()).ratio()
            similarity.append(sim)

        if len(similarity) == len(set(similarity)) :
            m = max(similarity)
            k = similarity.index(m)
        else :
            m = max(similarity)
            similar = []
            k = similarity.index(m)
            for x in range(len(similarity)) :
                if similarity[x] == m :
                    similar.append(x)

            maxi = 0
            for a in similar :
                if (di[str(a)][2]) > maxi :
                    maxi = di[str(a)][2]
                    k = a
    if di:
        pro = di[str(k)][0]
        price = di[str(k)][1]
    else:
	pro = "Not Found"
	price = "N/A"
    return pro, price


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id','username','password')

class ClientCouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ('client_coupon','client_id','phone_number')

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = ('id', 'company_name','sender_title','template_body')

class MessageSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField()

    class Meta:
        model = Messages
        fields = ('client_coupon','company_name','id', 'template', 'user_id', 'message_time' ,'message','date','time','vendor','name','orderId','sender','amount','scrapedName','scrapedPrice')

    def create(self, validated_data):
        try:
            pro = ''
            price = 0
            if str(validated_data['template']).lower() in ['amazon', 'myntra', 'snapdeal','paytm']:
		print '***************************************************************************'
	        print validated_data
		print '***************************************************************************'
		print extract(str(validated_data['template']).lower().strip(' ').strip('.').strip(' '), validated_data['name'].strip(' ').strip('.').strip(' '))
                pro, price = extract(str(validated_data['template']).lower().strip(' ').strip('.').strip(' '), validated_data['name'].strip(' ').strip('.').strip(' '))
	    elif str(validated_data['template']).lower() == 'flipkart':
	        pro = validated_data['name'].strip(' ').strip('.').strip(' ')
	        price = validated_data['amount']
            validated_data['scrapedPrice'] = price
            validated_data['scrapedName'] = pro
	    return Messages.objects.create(**validated_data)
        except Exception as e:
            PrintException()
