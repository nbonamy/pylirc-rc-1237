import lirc
from threading import Lock

class LircHandler:

  def __init__(self, config):
    self._config = config
    self._client = lirc.Client()
    self._command = None
    self._mutex = Lock()

  def handle(self, command):
    
    # avoid piling commands (especially for volume stuff)
    if self._mutex.acquire(blocking=False) == False:
      print(f'[LIRC] Previous command still processing. Dropping')
      return False
    
    try:

      # run command
      self._command = f'KEY_{command}' 
      print(f'[LIRC] Sending command {self._command}')
      self._client.send_once(self._config.get('lirc.device', 'Denon_RC-1237_raw'), self._command)
      return True
  
    except lirc.exceptions.LircdCommandFailureError as error:
      print(f'[LIRC] Error while executing LIRC command {self._command}')
      print(f'[LIRC] {error})') 
      return False
    
    finally:
      self._mutex.release()
      self._command = None
