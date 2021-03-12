import argparse
import re
import zlib
import binascii

"""
// Usage:
python2 deobfuscate.py -f <infile> [-o <outfile>]

* example
python2 deobfuscate.py -f data\kek.gay\setup.py -o data\kek.gay\obfuscated\setup.py
"""

parser = argparse.ArgumentParser(description='Deobfuscation.')
parser.add_argument('-f', '--infile', dest="infile" , required=True, help='Input file')
parser.add_argument('-o', '--outfile', dest="outfile", default = '' , help='Output file (optional)')
parser.add_argument('-I', '--ioc', dest="out_ioc_only", action='store_true', help='Output IOC only (optional)')
parser.add_argument('-S', '--script', dest="out_full_script", action='store_true', help='Output full script (optional)')
#parser.add_argument('-R', '--row', dest="include_row", action='store_true', help='Include row number (optional)')
parser.add_argument('-q', '--quiet', dest="quiet", action='store_true', help='Suppress output')

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

pattern_xor_compressed = re.compile("("+get_xor_data_fn_name(infile)+"\(zlib.decompress\([\"'][^\"']+[\"']\)\))")
pattern_compressed = re.compile("(zlib.decompress\([\"'][^\"']+[\"']\))")
#ssspattern_hex = re.compile(r"('(?:\\x[0-9a-z]{2})+')")


# obfuscated data
obf_list = fetch_data_by_regex(infile, pattern_xor_compressed)
print("")
file_content = open(infile, "r").read()

if len(args.outfile) > 0:
	f=open(args.outfile,"w")

for obf in obf_list:
	## extract the hex value
	data = obf[obf.index('\\x'):obf.rindex('\\x')+4]
	de_obf = deobfuscate(data)
	# output to console
	if not args.quiet:
		if not args.out_ioc_only:
			print(obf)
			print(de_obf+'\n')
		else:
			if len(de_obf) > 0:
				print(de_obf)

	if de_obf != '':
		# fix quotes around strings, default single quote.
		quote_chr = "'"
		if "'" in de_obf.strip():
			quote_chr = '"'
		if "\\'" in de_obf.strip():
			quote_chr = "'"
		if '\\"' in de_obf.strip():
			quote_chr = '"'

		if args.out_full_script:
			file_content = file_content.replace(obf, quote_chr+de_obf.strip()+quote_chr)

		if len(args.outfile) > 0 and not args.out_full_script:
			if not args.out_ioc_only:
				f.write("%s\n" % (obf))
				f.write("%s\r\n" % (de_obf))
			else:
				f.write("%s\n" % (de_obf))

if len(args.outfile) > 0:
	if args.out_full_script:
		f.write(file_content)
	f.close()
