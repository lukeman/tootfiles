# tootfiles.py
by [Luke Hatcher](http://lukehatcher.com)
Original blog post here: <http://lukehatcher.com/2009/05/storing-binary-data-in-your-twitter-stream/>

*Store your data in Twitter. Brilliant.*

Let's be honest: this is probably _the_ worst idea ever, but I laughed so hard
at the prospect of storing useful amounts of data in 140 byte text messages
that I had to see how it would work.

I don't think using this script is against the Twitter TOS, but I really can't be responsible if you somehow abuse things and screw it up for all of us. Don't pee in the pool, OK?

## Prerequisites

* python-twitter - Used to post tootfiles to Twitter HQ.
* simplejson - Used to parse toots in the decode process.
* BeautifulSoup - Used to scrape toots in the decode process. This might be removed in a later version, if I ever implement toots as linked-lists.

## Usage

This script can be used either as a standalone utility script or as a library.

### Standalone

#### Encoding a file to toots

To test encoding a file, simply pass the script a binary file with the `encode` flag and it will print the toot array to standard out. Go hog wild if you wish, but know that large files will generate a huge amount of output.

    python tootfiles.py -e helloworld.gif

To send that file to a Twitter stream, simply add your Twitter credentials using the `user` and `password` flags. I *highly* recommend setting up a second Twitter account to publish any data to. Small files are good here--keep it under 5KB for best results.

    python tootfiles.py -e helloworld.gif -u someuser  -p somepass

#### Decoding a published tootfile

To decode a published tootfile, you'll need to find a valid header status id to work with. I just happen to have one available, so we'll use it. Because we're playing nicely, the decoded file will go to standard out, but feel to redirect it to an actual file for your own purposes.

    python tootfiles.py -d 1670303405 > helloagainworld.gif
 
### As a code library

If you're interested in using tootfiles in another python project, you can stick its folder somewhere on your python path and just import it. The below code snippet outlines how to encode and decode using the library.

    import tootfiles
    
    # encode a file
    t = TootEncoder('filename')
    print t
    
    # publish said tootfile to twitter
    t.publish('username', 'password')
    
    # decode a file
    d = TootDecoder('12345678')  # arg is the tootfile headers
                                 # twitter status id
    print d
    
    # write it out with its original filename
    d.write()                    # if file exists, you must grant
    d.write(overwrite=True)      # overwrite privs, or it will error
    
    d.write('somenewfilename.out')
    d.write('somenewfilename.out', overwrite=True)


## License

This work is covered under the MIT license, which means you're free to do what you want with it. Libre, you dig?

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

#### Special Thanks
Special thanks goes to [Peter Burns](http://twitter.com/rictic) for taking a look at my code and making sure I didn't commit any high crimes or pythonic treason. His suggestions ultimately led to a better implementation of this awful idea.

Also, I should thank Scott Carpenter for [his blog post on scraping toots with BeautifulSoup](http://www.movingtofreedom.org/2009/03/18/python-script-for-backing-up-twitter-statuses/). I replaced my terribly poor initial method with his approach and cleaned up the code quite a bit.