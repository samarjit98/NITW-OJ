import socket
import os
import sys
import argparse
import random
import yaml
import errno
import time

YAML_FILE = './dictionary.yml'

testcases = [
		'./testcases/testcases1.txt',
		'./testcases/testcases2.txt'
	]

samples = [
		'./samples/sample1.c',
		'./samples/sample2.c'
	]

def handle_connection(cfd, cli_address):
	connection_table = {}
	with open(YAML_FILE, 'r') as ymlf:
		connection_table = yaml.load(ymlf)

	key = cfd.recv(4096).decode()
	if key not in connection_table:
		print("Wrong key!")
		return

	contents = cfd.recv(4096).decode()
	with open("./soln.c", "w") as f:
		f.write(contents)

	os.system("gcc ./soln.c -o soln")
	os.system("gcc " + samples[connection_table[key]-1] + " -o orig")

	f = open(testcases[connection_table[key]-1], "r")
	os.dup2(f.fileno(), sys.stdin.fileno())
	output_cli = os.popen("./soln", "r").read()
	f.close()

	f = open(testcases[connection_table[key]-1], "r")
	os.dup2(f.fileno(), sys.stdin.fileno())
	output_orig = os.popen("./orig", "r").read()
	f.close()

	if output_cli == output_orig:
		cfd.send("Success".encode())
	else:
		cfd.send("Failure".encode())
	

def connection_loop(port):
	sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sfd.bind(('localhost', port))
	sfd.listen(200)

	while True:
		cfd, cli_address = sfd.accept()
	
		pid = os.fork()
		if pid == 0:
			sfd.close()
			handle_connection(cfd, cli_address)
			cfd.close()

		cfd.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('port', type=int, help='server port')
	args = parser.parse_args()
	connection_loop(args.port)