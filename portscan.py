#https://docs.google.com/document/d/19JJUlr_MQSPjTnZ-4nfMJso7HXRdWoYgWBEr6I_EPiY/edit#heading=h.2j0nvxqbzuod
import socket
import select
from concurrent.futures import ThreadPoolExecutor, Future

def udp_check(host: str, port: int) -> bool:
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.sendto(b'\x1b'+47*b'\0', (host, port))
		r = select.select([s], [], [], 2)[0]
		if r:
			return True
		else:
			return False

def tcp_check(host: str, port: int) -> bool:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			s.settimeout(2)
			s.connect((host, port))
		except:
			return False
		return True
		
class Port:
	TCP = 0
	UDP = 1
	TCP_UDP = 2
	
	def __init__(self, port: int, tcp: bool = None, udp: bool = None):
		self.port = port
		self.tcp = tcp
		self.udp = udp
		
def scan(host: str, port1: int, port2: int, port_type: int, thread_count: int = None):
	'''port_type = Port.TCP || Port.UDP || Port.TCP_UDP'''
	
	from os import cpu_count
	port1, port2 = port1 if port2 > port1 else port2, port2 if port2 > port1 else port1
	if not thread_count:
		thread_count = min(cpu_count()*6, port2 - port1 + 1)

	if port_type == Port.TCP:
		def f(host, port):
			return Port(port, tcp=tcp_check(host, port))
	elif port_type == Port.UDP:
		def f(host, port):
			return Port(port, udp=udp_check(host, port))
	elif port_type == Port.TCP_UDP:
		def f(host, port):
			return Port(port, tcp=tcp_check(host, port), udp=udp_check(host, port))
	else:
		raise Exception('Wrong port_type')
	
	def handler(future: Future):
		port: Port = future.result()
		if port.tcp:
			print(f'{port.port} TCP')
		if port.udp:
			print(f'{port.port} UDP')
	with ThreadPoolExecutor(max_workers=thread_count) as pool:
		futures = [pool.submit(f, host, port).add_done_callback(handler) for port in range(port1, port2+1)]
		
HELP = '''-t для сканирования tcp
-u для сканирования udp
-p/--ports p1 p2 для указания диапазона сканирования, где [p1, p2] диапазон сканирования
-h host указывает хост/ip для сканирования
-T k для указания кол-ва потоков, k = 1, 2, 3...; не обязательный аргумент
примеры: 
portscan.py -t -u -p 20 100 -h example.com -T 40
portscan.py --ports 20 20 -u -T 4 -h example.com
portscan.py -h example.com --ports 20 21 -t'''

def main():
	from sys import argv
	host = False
	udp = False
	tcp = False
	port1 = False
	port2 = False
	thread_count = None
	i = 1
	try:
		while i < len(argv):
			if argv[i] == '-t':
				tcp = True
			elif argv[i] == '-u':
				udp = True
			elif argv[i] == '-h':
				host = argv[i+1]
				i+=1
			elif argv[i] == '-p' or argv[i] == '--ports':
				port1 = int(argv[i+1])
				port2 = int(argv[i+2])
				i+=2
			elif argv[i] == '-T':
				thread_count = int(argv[i+1])
				i+=1
			i += 1
	except:
		print(HELP)
		exit(1)
	port_type = None
	if udp and tcp:
		port_type = Port.TCP_UDP
	elif udp:
		port_type = Port.UDP
	elif tcp:
		port_type = Port.TCP
	else:
		print(HELP)
		exit(1)
	try:
		scan(host, port1, port2, port_type, thread_count)
	except socket.gaierror:
		print(f'{host} некорректный адрес')
		exit(1)
	except Exception as err:
		_exit = input('Возникли проблемы во время исполнения. Чтобы увидеть отчёт об ошибке нажмите Enter, иначе введите любой символ.')
		if _exit == '':
			print(err)
		exit(1)

if __name__ == '__main__':
	main()