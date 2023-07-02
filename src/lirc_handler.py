import lirc
from threading import Lock

class LircHandler:

  def __init__(self, config):
    self._config = config
    self._client = lirc.Client()
    self._command = None
    self._mutex = Lock()

  def send(self, command, repeat=None):
    
    # avoid piling commands (especially for volume stuff)
    if self._mutex.acquire(blocking=False) == False:
      print(f'[LIRC] Previous command still processing. Dropping')
      return False
    
    try:

      # command 
      self._command = f'KEY_{command}'

      # repeats
      if repeat is None:
        repeat = self._config.get(f'repeat.{self._command}')
      if repeat is None:
        repeat = 0
      elif isinstance(repeat, str):
        repeat = int(repeat)

      # run command
      obj = { 'command': self._command, 'repeat': repeat }
      print(f'[LIRC] Sending {obj}')
      self._client.send_once(self._config.get('lirc.device', 'Denon_RC-1237_raw'), self._command, repeat_count=repeat)
      return True
  
    except lirc.exceptions.LircdCommandFailureError as error:
      print(f'[LIRC] Error while executing LIRC command {self._command}')
      print(f'[LIRC] {error})') 
      return False
    
    finally:
      self._mutex.release()
      self._command = None
