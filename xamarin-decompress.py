import lz4.block
import os
import sys

#Usage
def printUsageAndExit():
	print("Check a file or directory for Xamarin .NET compressed assemblies and")
	print("decompresses them ready to decompile.")
	print("")
	print("Usage: xamarin-decompress.py [-o] <file-or-dir-path>")
	print("       If a file is specified, that file is decompressed, otherwise the")
	print("       directory is walked and all compressed .exe and .dll files are")
	print("       decompressed.")
	print("")
	print("       -o if specified, the original files will be overwritten with the")
	print("          decompressed data, otherwise the decompressed data will be written")
	print("          to <original-name>.decompressed.ext.")
	sys.exit(1)

#Check args
if len(sys.argv) < 2 or len(sys.argv) > 3:
	printUsageAndExit()

#Grab args
target = ""
overwrite = False
if len(sys.argv) == 3:
	if sys.argv[1] == "-o":
		overwrite = True
		target = sys.argv[2]
	elif sys.argv[2] == "-o":
		overwrite = True
		target = sys.argv[1]
	else:
		printUsageAndExit()
else:
	target = sys.argv[1]

#Check if a file is compressed and, if so, decompress it
def checkAndDecompress(filename):
	global overwrite
	print("Checking: " + filename)
	
	fh = open(filename, "rb")
	hdr = fh.read(8)
	print(hdr)
	if hdr[:4] == "XALZ".encode("utf-8"):
		print("[+] Found XALZ in header, decompressing...")
		dd = fh.read()
		fh.close()
		
		try:
			dd = lz4.block.decompress(dd)
			filenameout = filename
			if overwrite == False:
				filenameout = filename[:-3] + "decompressed" + filename[-4:]
			
			fh = open(filenameout, "wb")
			fh.write(dd)
			fh.close()
			print("[+] Decompressed assembly written to " + filenameout)
		except Exception as ex:
			print("[-] Decompression failed.\n" + str(ex))

#Check if the target is a file or directory
if os.path.isfile(target):
	checkAndDecompress(target)
else:
	for root, dirs, files in os.walk(target):
		for filename in files:
			if filename.lower().endswith(".exe") or filename.lower().endswith(".dll"):
				checkAndDecompress(os.path.join(root, filename))
