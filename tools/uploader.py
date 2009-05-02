#! /usr/bin/python

# http://fabien.seisen.org/python/urllib2_multipart.html

import os, sys
import urllib2_file
import urllib2
import simplejson

if len(sys.argv) != 3:
	print 'Usage: ./uploader.py <api_endpoint> <folder_or_file>'
	sys.exit(0)

def parse_cli_params():
	return sys.argv[1], sys.argv[2]

def do_file_upload(url, file):
	data = { 'file': open(file) }
	return simplejson.loads(urllib2.urlopen(url, data).read())

def folder_scanner(folder):
    if folder[0] == '.':
        folder = os.path.join( os.getcwd(), folder[2:] )
    for f in os.listdir(folder):
        if f[0] == '.':
            continue
        f = os.path.join(folder, f)
        if os.path.isdir(f):
            for x in folder_scanner(f):
                yield x
        if os.path.isfile(f):
            yield f

def check_result(r, f):
	if r['code'] != 0:
		print 'Error:', f
	else:
		print 'Ok:', f

def is_mp3(f):
	if f[-3:] == 'mp3':
		return True
	return False

def handle_file(f):
	if is_mp3(f):
		r = do_file_upload(url, f)
		check_result(r,f)
	else:
		print 'Ignore:', f

url, src = parse_cli_params()

if os.path.isfile(src):
	handle_file(src)
else:
	for f in folder_scanner(src):
		handle_file(f)

