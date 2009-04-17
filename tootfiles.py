#!/usr/bin/env python
# encoding: utf-8
"""
tootfiles - store binary data in a twitter stream
http://lukehatcher.com/

Copyright (c) 2009 Luke Hatcher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys
import os

import zlib
import base64
import md5
import re


def encode_file(filename):
    rawdata = open(filename, 'rb').read()
    md5hash = md5.new(rawdata).hexdigest()
    
    # Encode and split the data
    compressed_data = zlib.compress(rawdata,9)
    data = base64.b64encode(compressed_data)
    tootcount = (len(data)/140)+1 
    tootarray = [data[i*140:(i+1)*140] for i in range(tootcount)]
    
    # Header Information
    header = "Tootfile:'%s' MD5:'%s' Count:'%s'" % (filename, md5hash, tootcount)
    
    tootarray.insert(0, header) # Insert the header
    return tootarray

def decode_array(tootarray):
    data = "".join(tootarray[1:])
    compressed_data = base64.b64decode(data)
    raw_data = zlib.decompress(compressed_data)
    return raw_data
    
def tootinfo(tootarray):
    header_re = "Tootfile:'(?P<filename>.*?)' MD5:'(?P<md5>.*?)' Count:'(?P<count>.*?)'"
    results = re.compile(header_re).search(tootarray[0])
    return results.groupdict()
     

def main():
    toot = encode_file('helloworld.gif')
    newtoot = decode_array(toot)
    print tootinfo(toot)['md5'] == md5.new(newtoot).hexdigest()


if __name__ == '__main__':
	main()

