
import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
from http import HTTPStatus
from threading import Thread

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  pass

class HttpServer:

  def __init__(self, config, processor):
    self._config = config
    self._processor = processor
    self._server = None

  def delete(self):
    if self._server is not None:
      self._server.shutdown()
      self._server = None

  def start(self):
    port = self._config.get('http_server_port', 5007)
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.TCPServer.allow_reuse_port = True
    self._server = ThreadedTCPServer(('0.0.0.0', port), ApiHandler)
    self._server.processor = self._processor
    self._server_thread = Thread(target=self._server.serve_forever)
    self._server_thread.daemon = True
    self._server_thread.start()
    print(f'[HTTP] API server started at {port}')

class ApiHandler(http.server.BaseHTTPRequestHandler):

  def get_parameters(self):
    query = urlparse(self.path).query
    return dict((k, v[0] if isinstance(v, list) and len(v) == 1 else v)
      for k, v in parse_qs(query).items())

  def do_GET(self):

    # log
    print(f'[HTTP] {self.requestline}')

    # extract
    url_parts = urlparse(self.path)
    query_params = parse_qs(url_parts.query)

    # send
    if url_parts.path == '/api/send':
      self.process_send()
    else:
      # default
      self.error(HTTPStatus.NOT_FOUND)

  def process_send(self):
    command = self.get_parameters().get('command')
    repeat = self.get_parameters().get('repeat')
    if command is not None and self.server.processor(command, repeat):
      self.write_json({ 'status': 'ok', 'command': command })
    else:
      self.error()

  def write_json(self, payload):
    self.send_response(HTTPStatus.OK)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(bytes(json.dumps(payload).encode()))

  def error(self, code=HTTPStatus.INTERNAL_SERVER_ERROR):
    self.send_response(code)
    self.end_headers()

  def log_message(self, format, *args):
    pass
