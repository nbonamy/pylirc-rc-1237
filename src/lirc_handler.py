
import time
import lirc
from threading import Lock

class LircHandler:

  def __init__(self, config):
    self._config = config
    self._client = lirc.Client()
    self._command = None
    self._mutex = Lock()

  def send(self, command, repeat=None, duration=None):
    
    # avoid piling commands (especially for volume stuff)
    if self._mutex.acquire(blocking=False) == False:
      print(f'[LIRC] Previous command still processing. Dropping')
      return False

    try:

      # command 
      self._command = f'KEY_{command}'

      # duration (protect to not send too long)
      duration = duration if duration is not None else self._config.get(f'duration.{self._command}')
      duration = duration if duration is None or isinstance(duration, int) else int(duration)
      duration = duration if duration is None else min(2000, duration)

      # repeats
      repeat = repeat if repeat is not None else self._config.get(f'repeat.{self._command}')
      repeat = repeat if repeat is None or isinstance(repeat, int) else int(repeat)
      repeat = repeat if repeat is not None else 0

      # run command
      if duration is not None:
        self._send_duration(duration)
      else:
        self._send_repeat(repeat)      

      # done
      return True
  
    except lirc.exceptions.LircdCommandFailureError as error:
      print(f'[LIRC] Error while executing LIRC command {self._command}')
      print(f'[LIRC] {error})') 
      return False
    
    finally:
      self._mutex.release()
      self._command = None

  def _send_repeat(self, repeat):

    print(f'[LIRC] Sending {{ command: {self._command}, repeat: {repeat} }}')
    for i in range(repeat+1):
      self._client.send_once(self._config.get('lirc.device', 'Denon_RC-1237_raw'), self._command)
      if i < repeat:
        time.sleep(self._config.get('repeat.delay', 1000)/1000)

  def _send_duration(self, duration):

    print(f'[LIRC] Sending {{ command: {self._command}, duration: {duration} }}')
    self._client.send_start(self._config.get('lirc.device', 'Denon_RC-1237_raw'), self._command)
    time.sleep(duration/1000)
    self._client.send_stop()
