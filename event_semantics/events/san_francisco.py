import sys
from datetime import datetime
from time import mktime

def get_min_sec(seq):
	s = seq.split('.')
	minutes = s[0]
	seconds = (int(s[1])*60)/10000.0
	return int(minutes),int(seconds)
	
def to_degrees(pos,orientation):
	minutes,seconds = get_min_sec(pos[-7:])
	degrees = int(pos[:-7])
	m = -1 if orientation in ['S','W'] else 1
 	return "%.4f" % (m * (degrees + (minutes/60.0) + (seconds/3600.0)))

def get_unix_timestamp(time,datestamp):
	timestamp = time.split('.')[0]
	t = datetime.strptime(timestamp+datestamp,"%H%M%S%d%m%y")
	return mktime(t.timetuple())

if __name__ == '__main__':
	filename = sys.argv[1]
	f = open(filename, 'r')
	for line in f:
		traces = line.split('\r')
		for i in range(len(traces))[:-1]:
			data = traces[i].split(',')
			if data[0] == '$GPRMC':
				lat = to_degrees(data[3],data[4])
				lng = to_degrees(data[5],data[6])
				timestamp = get_unix_timestamp(data[1],data[9])
				print "%s %s %d" % (lat,lng,timestamp)
			else:
				continue
	f.close()

