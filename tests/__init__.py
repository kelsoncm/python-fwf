"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


# FILE01_CSV_EXPECTED = "codigo;nome\n1;um\n2;Dois\n3;três\n"
# FILE01_CSV_EXPECTED_BINARY = b'codigo;nome\n1;um\n2;Dois\n3;tr\xc3\xaas\n'
# FILE01_CSV_EXPECTED_LATIN1 = 'codigo;nome\n1;um\n2;Dois\n3;trÃªs\n'
#
#
# FILE02_JSON_EXPECTED = '["caça"]'
# FILE02_JSON_EXPECTED_LATIN1 = '["caÃ§a"]'
#
# FILE02_JSON_EXPECTED_BINARY = b'["ca\xc3\xa7a"]'
#
# CSV_EXPECTED = [{'codigo': '1', 'nome': 'um'}, {'codigo': '2', 'nome': 'Dois'}, {'codigo': '3', 'nome': 'três'}]
# JSON_EXPECTED = ['caça']
# ZIP_EXPECTED = b'PK\x03\x04\n\x00\x00\x00\x00\x00&z\xe9L\xad\rM\x07 \x00\x00\x00 \x00' \
#                b'\x00\x00\x08\x00\x1c\x00file.csvUT\t\x00\x03\xa8\xa6C[\xd6\xa6C[u' \
#                b'x\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00codigo;nome\n1;um\n2' \
#                b';Dois\n3;tr\xc3\xaas\nPK\x01\x02\x1e\x03\n\x00\x00\x00\x00\x00&z\xe9L\xad\r' \
#                b'M\x07 \x00\x00\x00 \x00\x00\x00\x08\x00\x18\x00\x00\x00\x00\x00\x01\x00' \
#                b'\x00\x00\xb4\x81\x00\x00\x00\x00file.csvUT\x05\x00\x03\xa8\xa6C[ux\x0b' \
#                b'\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00' \
#                b'\x01\x00\x01\x00N\x00\x00\x00b\x00\x00\x00\x00\x00'
