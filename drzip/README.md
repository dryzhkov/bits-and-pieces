### Data compressor that uses Huffman coding algorithm to compress and decompress text.

drzip.py - contains main logic for compression

bin.py - contains helpers for packing individual bits into bytes and unpacking them.

### Examples:

`cat text | ./drzip.py --compress`

`cat text | ./drzip.py --compress | ./drzip.py --decompress`
