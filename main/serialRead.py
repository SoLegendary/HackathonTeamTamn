import serial
import threading
import time
 
SERIAL_PORT = 'COM8'
BAUD_RATE = 115200
 
serial_content = []
def wait_on_serial():
    p = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    while True:
        serial_content.append(p.readline().rstrip(b'\n\r'))
 
#t = threading.Thread(target=wait_on_serial)
#t.daemon = True
#t.start()
 
def get_serial():
    if len(serial_content) > 0:
        return serial_content[-1]
 
def main():
  # while True:
  #      print get_serial()
  #      time.sleep(0.1)
  p = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
  while True:
    print p.readline().rstrip(b'\n\r')
    num = p.readline()
    if num is 'Reading Block 4:':
        string="booking_script.py " + 11988401
        cmd="echo " + string
        os.system(cmd)
         
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Done!"
        t.stop()
