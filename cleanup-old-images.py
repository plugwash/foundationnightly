#!/usr/bin/python3
import glob
import os
import re
from datetime import datetime, timedelta,time
from collections import OrderedDict
import operator

print('cleanup-old-images started')

basepath = '/usr/share/nginx/www/nightlyimages/'
files = glob.glob(basepath+'rpf-raspbian-nightly-????????-??????.img.xz')
basenames = [ os.path.basename(f) for f in files]
#print(files)
#print(basenames)

weeks = {} # datetime of first build from each week
months = {} # datetime of first build from each month
keep = {} # map of datetimes to whether we want to keep the build in question or not

# this pass determines what files exist (populating the keep map with entries of False) and finds the first build in each month
p=re.compile('[0-9]{8,8}-[0-9]{6,6}')
for name in basenames:
	m=p.search(name)
	dtstr = m.group()
	dt = datetime.strptime(dtstr,'%Y%m%d-%H%M%S');
	#print(dtstr)
	#print(dt)
	weekstart = (dt - timedelta(days = dt.weekday())).date()
	#rint(weekstart)
	#timesinceweekstart = dt-datetime.combine(weekstart,time(0,0,0,0));
	#print(timesinceweekstart)
	if not (weekstart in weeks):
		weeks[weekstart] = dt
	elif dt < weeks[weekstart]:
		weeks[weekstart] = dt
	monthstart = dt.replace(day=1);
	if not (monthstart in months):
		months[monthstart] = dt
	elif dt < months[monthstart]:
		months[monthstart] = dt
	keep[dt] = False

#keep the most recent 7 builds
for key,value in sorted(keep.items(),reverse=True)[:7]:
	keep[key] = True;

print

# keep first build from the most recent 4 weeks
weeks = sorted(weeks.items(),reverse=True)
for key,value in weeks[:4]:
	#print(value)
	keep[value] = True;

# keep first build from every month
for key,value in months.items():
	keep[value] = True;

keep = sorted(keep.items())

delete = []

print('list of images and whether they should be kept:')
for date,keepit in keep:
	datestr = date.strftime('%Y%m%d-%H%M%S')
	print(datestr+' '+str(keepit))
	if keepit == False:
		delete.append(datestr)

#sanity check in case of bugs, we should only be removing a maximum of one image under normal conditions
if len(delete) > 1:
	print('WARNING: '+str(len(delete))+'items in removal list but only removing one, bug?')
	delete = delete[:1]

for datestr in delete:
	files = glob.glob(basepath+'rpf-raspbian-nightly-'+datestr+'.*')
	for filename in files:
		print(filename)
		os.remove(filename)

print('cleanup-old-images complete');


