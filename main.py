#!/usr/bin/env python3

import sys
from src.utils import *
from src.http_server import HttpServer
from src.lirc_handler import LircHandler
from src.configuration import Configuration
from threading import Event

def main():

  server = None
  lirc = None
  tts = None

  def lirc_processor(command, repeat, duration):
    return lirc.send(command, repeat, duration)

  # load config
  config = Configuration(load_yaml('config/config.yml'))

  # init lirc
  lirc = LircHandler(config)

  try:

    # http server
    server = HttpServer(config, lirc_processor)
    server.start()

    # wait for ctrl-c
    Event().wait()

  except Exception as e:
    print(e)

  finally:
    safe_delete(server)
    safe_delete(lirc)
    safe_delete(config)
    
if __name__ == '__main__':
  main()
