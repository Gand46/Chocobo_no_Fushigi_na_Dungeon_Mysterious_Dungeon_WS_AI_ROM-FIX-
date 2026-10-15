"""Small deterministic BPS implementation. Only the Python standard library is needed.
Writer emits SourceRead/TargetRead; reader validates all four BPS action modes.
It is intentionally independent of the supplied ws_patch_tools reference decoder.
"""
from __future__ import annotations
import struct
import zlib


def crc(data: bytes | bytearray) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def encode_number(number: int) -> bytes:
    if number < 0:
        raise ValueError('A BPS number cannot be negative')
    result = bytearray()
    while True:
        digit = number & 127
        number >>= 7
        if number == 0:
            result.append(digit | 128)
            return bytes(result)
        result.append(digit)
        number -= 1


def create(source: bytes, target: bytes, metadata: bytes = b'') -> bytes:
    result = bytearray(b'BPS1')
    result += encode_number(len(source)) + encode_number(len(target))
    result += encode_number(len(metadata)) + metadata
    pos = 0
    while pos < len(target):
        same = pos < len(source) and source[pos] == target[pos]
        end = pos + 1
        while end < len(target) and (end < len(source) and source[end] == target[end]) == same:
            end += 1
        result += encode_number(((end - pos - 1) << 2) | (0 if same else 1))
        if not same:
            result += target[pos:end]
        pos = end
    result += struct.pack('<II', crc(source), crc(target))
    result += struct.pack('<I', crc(result))
    return bytes(result)


def apply(source: bytes, patch: bytes, max_output: int = 64 * 1024 * 1024) -> bytes:
    if len(patch) < 19 or patch[:4] != b'BPS1':
        raise ValueError('Invalid or truncated BPS header')
    if crc(patch[:-4]) != struct.unpack_from('<I', patch, len(patch) - 4)[0]:
        raise ValueError('Patch CRC32 mismatch')
    source_crc, target_crc = struct.unpack_from('<II', patch, len(patch) - 12)
    if crc(source) != source_crc:
        raise ValueError('Source CRC32 mismatch; use the declared Japanese ROM')
    pos = 4
    limit = len(patch) - 12

    def number() -> int:
        nonlocal pos
        value, weight = 0, 1
        for _ in range(10):
            if pos >= limit:
                raise ValueError('Truncated BPS integer')
            digit = patch[pos]
            pos += 1
            value += (digit & 127) * weight
            if digit & 128:
                return value
            weight <<= 7
            value += weight
        raise ValueError('BPS integer is too large')

    expected_source, target_size, metadata_size = number(), number(), number()
    if expected_source != len(source):
        raise ValueError('Source size mismatch')
    if target_size > max_output:
        raise ValueError('Target exceeds safety size limit')
    if pos + metadata_size > limit:
        raise ValueError('Truncated BPS metadata')
    pos += metadata_size
    output = bytearray()
    source_cursor = target_cursor = 0
    while len(output) < target_size:
        action = number()
        mode, count = action & 3, (action >> 2) + 1
        if len(output) + count > target_size:
            raise ValueError('BPS action exceeds declared target')
        if mode == 0:
            start = len(output)
            if start + count > len(source):
                raise ValueError('SourceRead is out of range')
            output += source[start:start + count]
        elif mode == 1:
            if pos + count > limit:
                raise ValueError('TargetRead is out of range')
            output += patch[pos:pos + count]
            pos += count
        else:
            encoded = number()
            delta = -(encoded >> 1) if encoded & 1 else encoded >> 1
            if mode == 2:
                source_cursor += delta
                if source_cursor < 0 or source_cursor + count > len(source):
                    raise ValueError('SourceCopy is out of range')
                output += source[source_cursor:source_cursor + count]
                source_cursor += count
            else:
                target_cursor += delta
                if target_cursor < 0 or target_cursor >= len(output):
                    raise ValueError('TargetCopy is out of range')
                for _ in range(count):
                    output.append(output[target_cursor])
                    target_cursor += 1
    if pos != limit:
        raise ValueError('Trailing bytes in BPS action stream')
    if crc(output) != target_crc:
        raise ValueError('Target CRC32 mismatch')
    return bytes(output)
