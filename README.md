# Arithmetic Coding - Integer Implementation
---
## How to Run
* Download Project Jupyter from https://jupyter.org/
* Download the Arithmetic_Coding_Jupyter.ipynb file from this repostory
* Launch Project Jupyter and load the Arithmetic_Coding_Jupyter.ipynb file and run each cell. (You can also run all but there are many cells which check output for compression ratio/correct output/etc and can clutter your screen.)
---
## Example output
Here is an example output of a compression and decompression of an 8 bytes sequence
![Image of simple compression and decompression](https://i.imgur.com/9W8m5dv.png)
---
## Arithmetic Coding 101 

Arithmetic coding is a form of entropy encoding used in lossless data compression. Normally, a string of characters such as the words "hello there" is represented using a fixed number of bits per character, as in the ASCII code. When a string is converted to arithmetic encoding, frequently used characters will be stored with fewer bits and not-so-frequently occurring characters will be stored with more bits, resulting in fewer bits used in total. Arithmetic coding differs from other forms of entropy encoding, such as Huffman coding, in that rather than separating the input into component symbols and replacing each with a code, arithmetic coding encodes the entire message into a single number, an arbitrary-precision fraction q where 0.0 ≤ q < 1.0. It represents the current information as a range, defined by two numbers.
 
 ---
## Integer Implementation

Instead of using a single arbitrary-precision fraction q to represent the current information integer implementation relys upon integer arithmetic to generate a binary code. 

I choose to use the integer implementation for two reasons:
1. It doesnt suffer from the same issues that non-adative arithmetic coding does. 
2. It is much more difficult to correctly implement.
---
