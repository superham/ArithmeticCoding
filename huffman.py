"""Minimal Huffman coding helpers used by the notebook.

Provides the four functions the notebook relies on:
    huffTree  – build a Huffman tree from a symbol-count mapping
    huffCode  – derive a {symbol: bitarray} code table from the tree
    make_tree – reconstruct a decoding tree from a code table
    decode    – walk the tree to decode a bitarray into symbols
"""
import heapq
from bitarray import bitarray


# ---- tree node ------------------------------------------------------------

class _Leaf:
    __slots__ = ("symbol",)

    def __init__(self, symbol):
        self.symbol = symbol

    # Comparisons needed so heapq tie-breaking never falls through to node
    def __lt__(self, other):
        return False


class _Internal:
    __slots__ = ("left", "right")

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __lt__(self, other):
        return False


# ---- public API -----------------------------------------------------------

def huffTree(counts):
    """Build a Huffman tree from *counts* (``{symbol: count}``)."""
    heap = [(count, _Leaf(sym)) for sym, count in counts.items() if count > 0]
    heapq.heapify(heap)

    if len(heap) == 0:
        raise ValueError("counts must contain at least one non-zero entry")

    while len(heap) > 1:
        w1, n1 = heapq.heappop(heap)
        w2, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, _Internal(n1, n2)))

    return heap[0][1]


def huffCode(tree):
    """Return ``{symbol: bitarray}`` prefix codes from *tree*."""
    codes = {}

    def _walk(node, prefix):
        if isinstance(node, _Leaf):
            # Single-symbol alphabet: assign a 1-bit code.
            codes[node.symbol] = bitarray(prefix) if prefix else bitarray("0")
            return
        _walk(node.left, prefix + "0")
        _walk(node.right, prefix + "1")

    _walk(tree, "")
    return codes


def make_tree(code_table):
    """Reconstruct a binary decoding tree from a ``{symbol: bitarray}`` table."""
    root = [None, None]  # [left, right]

    for symbol, bits in code_table.items():
        node = root
        for bit in bits[:-1]:
            idx = int(bit)
            if node[idx] is None:
                node[idx] = [None, None]
            node = node[idx]
        node[int(bits[-1])] = symbol

    return root


def decode(tree, bits):
    """Decode *bits* (a ``bitarray``) using the decoding *tree*.

    Returns a list of symbols.  The caller is responsible for locating
    any end-of-sequence marker.
    """
    symbols = []
    node = tree

    for bit in bits:
        node = node[int(bit)]
        if not isinstance(node, list):
            symbols.append(node)
            node = tree

    return symbols
