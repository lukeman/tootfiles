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

# External dependency, see README.md
import twitter

class FileEncoder(object):
    def __init__(self, filename):
        super(FileEncoder, self).__init__()
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
        header = "Tootfile:'%s' MD5:'%s' Count:'%s'" % (self.filename, md5hash, self.tootcount)

        tootlist.append(header) # Insert the header
        self.tootlist = tootlist
        
    def _segment(self, data, n=140):
        ''' Given the encoded string, slice it into twitter ready array elements '''
        self.tootcount = int(math.ceil(len(data)/float(n)))
        slices = range(self.tootcount,0,-1)
        
        return [data[i*n:(i+1)*n] for i in slices]
    
    def PublishToot(self, username, password):
        api = twitter.Api(username, password)
        
        for toot in self.tootlist:
            api.PostUpdate(toot)
    
    def __unicode__(self):
        for toot in self.tootlist:
            print toot
                
        
class TootDecoder(object):
    def __init__(self, tootdata):
        super(TootDecoder, self).__init__()
        self._processheader()
    
    def _get_info(tootarray):
        header_re = "Tootfile:'(?P<filename>.*?)' MD5:'(?P<md5>.*?)' Count:'(?P<count>.*?)'"
        results = re.compile(header_re).search(tootarray[0])
        self.headerinfo = results.groupdict()


def decode_array(tootarray):
    data = "".join(tootarray[1:])
    compressed_data = base64.b64decode(data)
    raw_data = zlib.decompress(compressed_data)
    return raw_data
     

def main():
    # TODO


if __name__ == '__main__':
	main()

