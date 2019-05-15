import socket
import os
import sys
import argparse
import time

def handle_connection(port, file, key):
	sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sfd.connect(('localhost', port))
	f = open(file, "r")

	contents = f.read()
	sfd.send(str(key).encode())
	time.sleep(0.05)
	sfd.send(contents.encode())
	time.sleep(0.05)

	mesg = sfd.recv(4096)
	print("Your result: {}".format(mesg.decode()))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('port', type=int, help='server port')
	parser.add_argument('file', help='path to C file')
	parser.add_argument('key', help='unique key')
	args = parser.parse_args()

	handle_connection(args.port, args.file, args.key)
