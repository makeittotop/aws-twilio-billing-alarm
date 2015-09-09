#!/usr/bin/env python

import os, sys
import boto
from boto.s3.key import Key

if len(sys.argv) != 3:
  print "Usage: <script> <bucket> <dir>"
  sys.exit(1)

bucket_name = sys.argv[1]
dir = sys.argv[2]

try:
  c = boto.connect_s3()
  bucket = c.get_bucket(bucket_name)
except Exception as e:
  print "Error: ", e.message
  sys.exit(1)

matches = []
for root, dirnames, filenames in os.walk(dir):
  for filename in filenames:
    matches.append(os.path.join(root, filename))

for match in matches:
  if not bucket.get_key(match):
    print "Creating key: ", match, " in bucket: ", bucket_name
    k = Key(bucket)
    k.key = match
    k.set_contents_from_filename(match)
  else:
    print "Key: ", match, " exists in bucket: ", bucket_name

print "Done!"


