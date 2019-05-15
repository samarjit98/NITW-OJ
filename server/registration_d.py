import socket
import os
import sys
import argparse
import random
import yaml
import errno
import time

YAML_FILE = './dictionary.yml'
NUM_QUES = 2

questions = [
		'./questions/question1.txt',
		'./questions/question2.txt'
	]

connection_table = {}

def handle_connection(cfd, cli_address):
	(host, port) = cli_address
	key = host + "@" + str(port) 
	qno = random.randrange(1, NUM_QUES+1, 1)
	f = open(questions[qno-1], "r")
	contents = f.read()
	
	cfd.send(key.encode())
	time.sleep(0.05)
	cfd.send(str(qno).encode())
	time.sleep(0.05)
	cfd.send(contents.encode())

	connection_table[key] = qno
	with open(YAML_FILE, 'w') as ymlf:
		yaml.dump(connection_table, stream=ymlf, default_flow_style=False)

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