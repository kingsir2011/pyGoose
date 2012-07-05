import logging
import re
import extractor

class Configuration(object):
    """docstring for Configuration"""
    def __init__(self):
        super(Configuration, self).__init__()
        self.headers = { 
                    'accept-language': 'en-us,en;q=0.5', 
                    'dnt': '1', 'keep-alive': '115', 
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 
                    'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
        }
        self.pubdateextractor = extractor.PublishDateExtractor()

from urllib.request import urlopen, Request
from exception import NotFoundException

class HTMLFetcher(object):
    """docstring for HTMLFetcher"""
    def __init__(self):
        super(HTMLFetcher, self).__init__()

    
    def getHTML(self,config,parsecandidate):
        hashChar = parsecandidate.url.find('#')
        if(hashChar>=0):
            url = parsecandidate.url[0:hashChar]
        else:
            url = parsecandidate.url

        try:
            #empty cookie store?
            #get http response
            request = Request(url,None, config.headers)
            response = urlopen(request)
            if response.getcode() == 404:
                raise NotFoundException(url)
            #find character encode
            contenttype = response.getheader('content-type')
            if contenttype and contenttype.find('charset') >=0 :
                parsecandidate.charset = contenttype[contenttype.find('charset'):]

            return response.readall()
        except NotFoundException as e:
            logging.error("Link not found (404): " + e.url) 
            raise e
        except Exception as e:
            raise e

class ParsingCandidate(object):
    """docstring for ParsingCandidate"""
    def __init__(self, urlstr, linkhash, url):
        super(ParsingCandidate, self).__init__()

        self.urlstr  = urlstr   
        self.linkhash = linkhash
        self.url = url

from hashlib import md5
class URLHelper(object):
    """docstring for URLHelper"""
    def __init__(self):
        super(URLHelper, self).__init__()
    

    def getcleanedurl(self, url):
        """the use of a cleaned url is not obvious now, let see """
        try:
            if(url.find('#!')>=0):
                clearnUrl = re.sub(r'#!', r'?_escaped_fragment=',url)
            else:
                clearnUrl = url

            return ParsingCandidate(clearnUrl, md5(url.encode('utf-8')), url)
        except Exception as e:
            logging.critical("Error in parsing url " + str(url))
            raise e
            
        