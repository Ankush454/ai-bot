
import requests
from bs4 import BeautifulSoup
import urllib, urllib2


def weather_report(place):
    print 'called'
    query = '{} weather forecast'.format(place)
    address = "http://www.google.com/search?q=%s&num=100&hl=en&start=0" % (urllib.quote_plus(query))
    request = urllib2.Request(address, None, {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0'})
    page = urllib2.urlopen(request).read()

    soup = BeautifulSoup(page, "lxml")
    try: 
        wind = soup.find('span', attrs={ 'id':'wob_ws'}).text
        plc = soup.find('div', attrs={ 'id':'wob_loc'}).text
        # c = soup.find('span', attrs={ 'class':'wob_t'}).text
        status = soup.find('span', attrs={ 'id':'wob_dc'}).text
        temp = soup.find('span', attrs={ 'id':'wob_tm'}).text
        hm = soup.find('span', attrs={ 'id':'wob_hm'}).text
        print plc
        try:
        	temp = ((int(temp) - 32) * 5/9)
        except:
        	pass
        context = {'temp':temp, 'wind':wind, 'status':status, 'hm':hm, 'plc':plc}
        return [context, True]
    except:
        context = {}
        return [context, False]

