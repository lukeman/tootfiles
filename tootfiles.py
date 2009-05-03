#!/usr/bin/env python
# encoding: utf-8
"""
tootfiles - store binary data in a twitter stream
http://lukehatcher.com/
"""

import sys
import getopt
import os
import math
import re
import zlib
import base64
import md5
import time
import urllib
from optparse import OptionParser


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

        slices = range(self.tootcount)
        slices.reverse()
        
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
                    

    def __str__(self):
        return "\n".join([toot for toot in self.tootlist])
                
        
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
    
    def __str__(self):
        return self.rawdata
            
    
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
        
        
def encode(filename, username=None, password=None):
    if not os.path.exists(filename):
        raise Exception("Specified input file does not exist")
    
    t = TootEncoder(filename)
    
    if username is not None and password is not None:
        t.publish(username, password)
    else:
        print(t)

def decode(tootid):
    """Given a Twitter status ID, attempt to decode"""
    t = TootDecoder(tootid)
    t.retrieve()
    print t

def main(argv=None):
    usage = "usage: %prog [-d tootidtodecode] or [-e 'somefile' -u 'username' -p 'password']"
    
    parser = OptionParser(usage=usage)
    parser.add_option("-e", dest="filename", metavar="filename", default=None,
                      help="The name of the file you wish to encode")
    parser.add_option("-u", dest="username", metavar="username", default=None,
                      help="A valid Twitter username")
    parser.add_option("-p", dest="password", metavar="password", default=None,
                      help="The password to your twitter account")
    parser.add_option("-d", dest="tootfileid", metavar="id", default=None,
                      help="Twitter ID of header to decode from")
    (options, args) = parser.parse_args()
    
    encoding = options.filename is not None
    decoding = options.tootfileid is not None
    havepass = options.password is not None
    haveuser = options.password is not None
    
    # This will catch cases where both encode and decode are selected and where neither is
    if encoding is decoding:
        parser.error("You must choose to either encode or decode. Use --help for more info.")
    
    if decoding:
        # Decode a file from the header with Twitter ID tootfileid
        # and print to stdout
        decode(options.tootfileid)
    elif encoding and haveuser and havepass:
        # Encode a file and publish to Twitter
        encode(options.filename, options.username, options.password)
    elif encoding:
        # Encode a file and print to stdout
        encode(options.filename)
        
if __name__ == "__main__":
    sys.exit(main())
