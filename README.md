# Python LZSS

A simple Python implementation of the [LZSS algorithm](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Storer%E2%80%93Szymanski).

Please check out this [blog post](https://tim.cogan.dev/lzss) for a walk through of the code.

## Install

`pip install lzss-python`

## Use

```python
>>> import lszz
>>> compressed = lzss.compress(b'my data my data my data')
>>> compressed
b'6\x9eD\x06C\t\xd0\xc2 \x80F\x80'
>>> lzss.decompress(compressed)
b'my data my data my data'
```