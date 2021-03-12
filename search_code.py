import argparse
import re
import zlib
import binascii

"""
// Usage:
python2 deobfuscate.py -f <infile> [-o <outfile>] -s <search phrase>

* example
python2 deobfuscate.py -f data\kek.gay\setup.py -o data\kek.gay\obfuscated\setup.py
"""

parser = argparse.ArgumentParser(description='Deobfuscation.')
parser.add_argument('-f', '--infile', dest="infile", required=True, help='Input file')
parser.add_argument('-s', '--search', dest="search_for", required=True, help='search phrase')
parser.add_argument('-o', '--outfile', dest="outfile", default = '', help='Output file (optional)')
parser.add_argument('-a', '--append', dest="out_append", action='store_true', help='Append to output file')
parser.add_argument('-A', '--out-after', dest="out_after", type=int, default = 0, help='Out num of rows after search hit')

args = parser.parse_args()

infile = args.infile
outfile = args.outfile

def xor_data(s):
	dec_list = [212, 55, 14, 121, 109, 247, 119, 92, 152, 42, 175, 149, 49, 242, 43, 70, 250, 248, 68]
	data = ''.join([chr(ord(c) ^ dec_list[i % len(dec_list)]) for i, c in enumerate(s)]).strip().replace("\n","\\n")
	if len(data) < 1:
		return ''
	try:
		return data.decode()
	except:
		return ''

def unhex(s):
	s_hex = s.replace("\\x", "").strip()
	return binascii.unhexlify(s_hex)

def decompress(s):
	return zlib.decompress(s)

def deobfuscate(s):
	return xor_data(decompress(unhex(s)))

def get_xor_data_fn_name(infile):
	fn_row = -1
	pattern = "\[212, 55, 14, 121, 109, 247, 119, 92, 152, 42, 175, 149, 49, 242, 43, 70, 250, 248, 68\]"
	for i, line in enumerate(open(infile)):
		for match in re.finditer(pattern, line):
			fn_row = i-1
			break
	if fn_row > -1:
		fn_line = open(infile).readlines()[fn_row]
		return re.findall(" (.*)\(", fn_line.strip())[0]
	return None

def fetch_data_by_regex(infile, pattern):
	result = []
	for i, line in enumerate(open(infile)):
		for match in re.finditer(pattern, line):
			result += match.groups()
	return result

def search_file(infile, pattern):
	result = []
	for i, line in enumerate(open(infile)):
		for match in re.finditer(pattern, line):
			if i not in result:
				result.append(i)
	return result

pattern_xor_compressed = re.compile("("+get_xor_data_fn_name(infile)+"\(zlib.decompress\([\"'][^\"']+[\"']\)\))")
pattern_compressed = re.compile("(zlib.decompress\([\"'][^\"']+[\"']\))")
#ssspattern_hex = re.compile(r"('(?:\\x[0-9a-z]{2})+')")

rows = search_file(infile, args.search_for)
file_content = open(infile).readlines()
if len(args.outfile) > 0:
	open_mode = "w"
	if args.out_append:
		open_mode = "a+"
	f=open(args.outfile,open_mode)

print(' [*] : %s' % (args.search_for))
if len(args.outfile) > 0:
	f.write(' [*] : %s\n' % (args.search_for))

for row in rows:
	print(' [%s] : %s' % (row+1, file_content[row]))
	if len(args.outfile) > 0:
		f.write(' [%s] : %s' % (row+1, file_content[row]))

	if args.out_after > 0:
		for i in range(args.out_after):
			print('+[%s] : %s' % (row+1+i+1, file_content[row+i+1]))
			if len(args.outfile) > 0:
				f.write('+[%s] : %s' % (row+1+i+1, file_content[row+i+1]))

if len(args.outfile) > 0:
	f.close()
