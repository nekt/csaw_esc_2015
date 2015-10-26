#! /usr/bin/env python
# execute as root to bind; the first 
# argument is the interface name to bind

import socket, sys, binascii

def main():
  if len(sys.argv) < 2:
    print "The interface name is missing."
    sys.exit(1)
  
  try:
    soc = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
  except socket.error as msg:
    print msg, "[socket]"

  try:
    soc.bind((sys.argv[1], 0x0800))
  except socket.error as msg:
    soc.close()
    print msg, "[bind]"
    
  if soc is None:
    print '[socket is None]'
    soc.close()

  print "Waiting for packets..."
  while 1:  
    try:
      data, addr = soc.recvfrom(2048)
    except socket.error as msg:
      print msg, "[recvfrom]"
      break
    if not data:
      print "[No data received]" 
      break

    print "*Received* ", binascii.hexlify(data)


if __name__ == '__main__':
  main()
