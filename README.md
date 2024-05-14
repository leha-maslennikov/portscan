# portscan.py

# Как запускать
## 1 Командная строка
python3 portscan.py аргументы
-t для сканирования tcp
-u для сканирования udp
-p/--ports p1 p2 для указания диапазона сканирования, где [p1, p2] диапазон сканирования
-h host указывает хост/ip для сканирования
-T k для указания кол-ва потоков, k = 1, 2, 3...; не обязательный аргумент
примеры: 
portscan.py -t -u -p 20 100 -h example.com -T 40
portscan.py --ports 20 20 -u -T 4 -h example.com
portscan.py -h example.com --ports 20 21 -t'''
## 2 Метод scan
Вызываем метод scan(host: str, port1: int, port2: int, port_type: int, thread_count: int = None)
host указывает хост/ip для сканирования
[port1, port2] диапазон сканирования
port_type = Port.TCP || Port.UDP || Port.TCP_UDP
thread_count кол-во потоков

# Тесты
Результат тестирования portscan.png. Для проверки ответов использовались:
###  https://www.networkcenter.info/index
###  https://ivit.pro/services/avail-services/

# Было реализовано
[1-2 балла] список открытых TCP-портов
[1-4 балла] список открытых UDP-портов
[1-3 балла] многопоточность
# Не было реализовано
[1-6 балла] распознать прикладной протокол по сигнатуре 
