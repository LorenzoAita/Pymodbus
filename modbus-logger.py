#!/usr/bin/python

PROXIMITY = 5

#requires pymodbus3...pip install pymodbus3
from pymodbus3.client.sync import ModbusTcpClient


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('ip_address', type=str, help='IP address of Modbus TCP server')
parser.add_argument('registers', type=str, help='Comma seperated string of registers to read, the first character of each address indicates the type of register (0=, 1=, 3=, 4=)')
parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
parser.add_argument('-u', '--unit', type=int, default=1, help='Modbus unit id (default is 1)')
parser.add_argument('-p', '--port', type=int, default=502, help='Modbus port to connect to (default is 502)')
parser.add_argument('-i', '--interval', type=int, default=1000, help='Read interval in milliseconds (default is 1000)')
parser.add_argument('-f', '--file', help='Filename to output data to')
parser.add_argument('-s', '--separator', default=',', help='Separator character (default is ,)')
args = parser.parse_args()


#data = dict((x.strip(), '-') for x in args.registers.split(','))

#print(data)
#exit()

import re
p = re.compile('^(\d)(\d+)$')

registerList = []
readList = []


for r in args.registers.split(','):
	a = p.match(r.strip())
	if a:
		nr = {'type': int(a.group(1)), 'address': int(a.group(2)), 'count': 1}
		registerList.append(nr)
		for ri in readList:
			if ri['type'] == nr['type']:
				if (nr['address'] < ri['address']) and (ri['address'] <= nr['address'] + PROXIMITY):
					ri['count'] += ri['address'] - nr['address']
					ri['address'] = nr['address']
					nr = None
					break
				elif (nr['address'] > ri['address']) and (ri['address'] + ri['count'] > nr['address'] - PROXIMITY):
					ri['count'] = max(ri['count'], nr['address'] - ri['address'] + 1)
					nr = None
					break
		if nr:
			readList.append(nr)

if args.verbose:
	print(registerList)
	print(readList)

import datetime
from time import sleep
import signal
import sys
def signal_handler(signal, frame):
	print('\nExiting!')
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


client = ModbusTcpClient(args.ip_address, args.port)

data = {}
lastFilename = ''
while True:
	for ri in readList:
		result = '-'
		if ri['type'] == 0:
			result = client.read_coils(ri['address'], ri['count'], unit=args.unit)

		if result != '-':
			i = 0
			for r in result.bits:
				data[str(ri['type']) + '_' + str(ri['address'] + i)] = str(int(r))
				i += 1

	curTime = datetime.datetime.now()
	output = curTime.strftime('%Y-%m-%d')
	output += ',' + curTime.strftime('%H:%M:%S')
	for r in registerList:
		output += ',' + data[str(r['type']) + '_' + str(r['address'])]

	if args.file:
		fileName = curTime.strftime(args.file)
		if lastFilename == '':
			lastFilename = fileName

		file = None
		if lastFilename != fileName:
			file = open(curTime.strftime(args.file), 'w+')
			lastFilename = fileName
		else:
			file = open(curTime.strftime(args.file), 'a+')

		file.write(output + '\n')
		file.close()
	else:
		print(output)

	sleep(args.interval / 1000)

client.close()
