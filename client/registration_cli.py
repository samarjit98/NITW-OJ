import socket
import os
import sys
import argparse

def handle_connection(port):
	sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sfd.connect(('localhost', port))

	mesg = sfd.recv(4096)
	print("Your unique key: {}".format(mesg.decode()))
	qno = sfd.recv(4096)
	print("Question number: {}".format(qno.decode()))
	desc = sfd.recv(4096)
	print("Question description: {}".format(desc.decode()))

	sfd.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('port', type=int, help='server port')
	args = parser.parse_args()
	handle_connection(args.port)