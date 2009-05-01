# tootfiles.py

*Store your data in Twitter.*

Let's be honest: this is probably _the_ worst idea ever, but I laughed so hard
at the prospect of storing useful amounts of data in 140 byte text messages
that I had to see how it would work.

I don't think using this script is against the Twitter TOS, but I really can't be responsible if you somehow abuse things and screw it up for all of us. Don't pee in the pool, OK?

# Usage

This script can be used either as a standalone utility script or as a library.

## Standalone

### Encoding a file to toots

To test encoding a file, simply pass the script a binary file with the `encode` flag and it will print the toot array to standard out. Go hog wild if you wish, but know that large files will generate a huge amount of output.

    python tootfiles.py --encode="helloworld.gif"

To send that file to a Twitter stream, simply add your Twitter credentials using the `user` and `password` flags. I *highly* recommend setting up a second Twitter account to publish any data to. Small files are good here--keep it under 5KB for best results.

    python tootfiles.py --encode="helloworld.gif" --user="someuser" --password="somepass"

### Decoding a published tootfile

To decode a published tootfile, you'll need to find a valid header status to work with. I just happen to have one available, so we'll use it. Because we're playing nicely, the decoded file will go to standard out, but feel to redirect it to an actual file for your own purposes.

    python tootfiles.py --decode="http://someurl.com" > helloagainworld.gif
 
## As a code library

If you're interested in using tootfiles in another python project, you can stick its folder somewhere on your python path and just import it. The below code snippet outlines the API.

    import tootfiles


# License

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