# Modbus Data Logger #

This script is a simple Modbus data logger that will poll data from any Modbus TCP device and write that data to CSV files.

For more information, please visit:  https://kgmoney.net/projects/modbus-data-logger


./modbus-data-logger.py -h

usage: modbus-data-logger.py [-h] [-v] [-u UNIT] [-p PORT] [-i INTERVAL]
[-f FILE] [-s SEPARATOR]
ip_address registers

positional arguments:

ip_address IP address of Modbus TCP server

registers Comma seperated string of registers to read, the first

character of each address indicates the type of

register (0=Coil, 1=Discreet Input, 3=Input Register, 4=Holding Register)

optional arguments:

-h, --help show this help message and exit

-v, --verbose Increase output verbosity

-u UNIT, --unit UNIT Modbus unit id (default is 1)

-p PORT, --port PORT Modbus port to connect to (default is 502)

-i INTERVAL, --interval INTERVAL

Read interval in milliseconds (default is 1000)

-f FILE, --file FILE Filename to output data to

-s SEPARATOR, --separator SEPARATOR

Separator character (default is ,)



This project is released under the MIT license.