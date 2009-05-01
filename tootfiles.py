#!/usr/bin/env python
# encoding: utf-8
"""
tootfiles - store binary data in a twitter stream
http://lukehatcher.com/
"""

import sys
import os
import math
import re
import zlib
import base64
import md5
import time
import urllib

# External dependencies, see README.md
import simplejson as json
from BeautifulSoup import BeautifulSoup
import twitter

class TootEncoder(object):
    def __init__(self, filename):
        super(TootEncoder, self).__init__()
        self.filename = filename
        self._encode()
    
    def _encode(self):
        sourcefile = open(self.filename, 'rb')
        rawdata = sourcefile.read()
        sourcefile.close()
        
        md5hash = md5.new(rawdata).hexdigest()

        # Encode and split the data
        compressed_data = zlib.compress(rawdata,9)
        data = base64.b64encode(compressed_data)
        tootlist = self._segment(data)

        # Header Information
        header = "|Tootfile:'%s' MD5:'%s' Count:'%s'|" % (self.filename, md5hash, self.tootcount)

        tootlist.append(header) # Insert the header
        self.tootlist = tootlist
        
    def _segment(self, data, n=140):
        ''' Given the encoded string, slice it into twitter ready array elements '''
        self.tootcount = int(math.ceil(len(data)/float(n)))
        slices = range(self.tootcount,0,-1)
        slices.reverse()
        slices = range(self.tootcount)
        slices.reverse()
        print slices
        
        return [data[i*n:(i+1)*n] for i in slices]
    
    def publish(self, username, password):
        api = twitter.Api(username, password)
        print "Publishing '%s' to %s's stream with %s segments..." % (self.filename, username, self.tootcount) 
        for toot in self.tootlist:
            # Occasionally, Twitter will either throttle us or throw an error.
            # For now, we'll handle all exceptions and simply retry. This should
            # be improved in the future.
            for retries in range(5):
                try:
                    #print "Attempting to publish '%s' with length %s" % (toot, len(toot))
                    status = api.PostUpdate(toot)
                    print '.',
                    break
                except:
                    if retries == 4:
                        raise Exception('Unable to post a segment. Quitting.')
                    else:
                        # Let's wait a bit before trying again
                        time.sleep(1)
        print "Finished."
                    
    
    def __unicode__(self):
        for toot in self.tootlist:
            print toot
                
        
class TootDecoder(object):
    def __init__(self, headerid):
        super(TootDecoder, self).__init__()
        self.headerid = headerid
        self.tootlist = []
        self._grabheader()
        self._getinfo()
    
    def retrieve(self):
        """Retrieve toot data from Twitter"""
        if self.headerid is not None:
            self._walk()
            self._decode()
    
    def write(self, filename=None, overwrite=False):
        if(self.md5hash == self.headerinfo['md5']):
            if filename is None:
                filename = self.headerinfo['filename']
            if not overwrite and os.path.exists(filename):
                raise Exception("File exists. Will not overwrite. Specify permission with overwrite set to true.")
            f = open(filename,'wb')  
            f.write(self.rawdata)
            f.close()
            
    
    def _grabheader(self):
        """Takes the headerid and retrieves the header text"""
        raw = urllib.urlopen('http://twitter.com/statuses/show/%s.json' % self.headerid)
        js = raw.readlines()
        js_object = json.loads(js[0])
        self.headerdata = js_object['text']
        #print self.headerdata
        self.username = js_object['user']['screen_name']
    
    def _getinfo(self):
        header_re = "\|Tootfile:'(?P<filename>.*?)' MD5:'(?P<md5>.*?)' Count:'(?P<count>\d+)'\|"
        results = re.match(header_re, self.headerdata)
        self.headerinfo = results.groupdict()
    
    def _walk(self):
        grabbedtoots = 0
        
        url = 'http://twitter.com/%s?page=%s'
        re_status_id = re.compile(r'.*/status/([0-9]*).*')
        
        maxpages = int(math.ceil(int(self.headerinfo['count'])/20.0))
        for page in range(1,maxpages+1):
            f = urllib.urlopen(url % (self.username, page))

            soup = BeautifulSoup(f.read())
            f.close()
            toots = soup.findAll('li', {'class': re.compile(r'.*\bstatus\b.*')})
            if len(toots) == 0:
                break

            for toot in toots:
                if grabbedtoots < int(self.headerinfo['count']):
                    m = re_status_id.search(toot.find('a', 'entry-date')['href'])
                    status_id = m.groups()[0]

                    if(int(status_id) < int(self.headerid)):
                        data = str(toot.find('span', 'entry-content').renderContents())
                        self.tootlist.append(data)
                        grabbedtoots += 1
                else:
                    break

            # small delay between pages 
            time.sleep(1)
    def _decode(self):
        """Decodes the raw data from the Twitter stream"""
        data = "".join(self.tootlist)
        compressed_data = base64.b64decode(data)
        self.rawdata = zlib.decompress(compressed_data)
        self.md5hash = md5.new(self.rawdata).hexdigest()
        
        
     

def main():
    # TODO


if __name__ == '__main__':
	main()

