import lirc

class LircHandler:

  def __init__(self, config):
    self._config = config
    self._client = lirc.Client()

  def handle(self, command):
    try:
      print(f'[LIRC] Sending command {command}')
      self._client.send_once(self._config.get('lirc.device', 'Denon_RC-1237_raw'), command)
      return True
    except lirc.exceptions.LircdCommandFailureError as error:
      print(f'[LIRC] Error while executing LIRC command {command}')
      print(f'[LIRC] {error})') 
      return False
