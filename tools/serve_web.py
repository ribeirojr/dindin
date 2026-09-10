"""Servidor da versao web, acessivel na rede local (celular, tablet).

O http.server padrao e single-thread: uma requisicao pendurada trava as
outras, e o Pyodide baixa varios arquivos de uma vez. Aqui usa a versao
com threads e imprime o endereco pra abrir no celular.
"""

import socket
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "web"
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # Sem cache: o celular pega a versao nova a cada refresh.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write(f"  {self.address_string()} {fmt % args}\n")


def ip_local() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main() -> None:
    handler = partial(Handler, directory=str(RAIZ))
    servidor = ThreadingHTTPServer(("0.0.0.0", PORTA), handler)
    servidor.daemon_threads = True
    ip = ip_local()
    print(f"DinDin servindo {RAIZ}")
    print(f"  neste Mac:  http://localhost:{PORTA}")
    print(f"  no celular: http://{ip}:{PORTA}")
    print("  (ctrl+c pra parar)\n")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nparado.")


if __name__ == "__main__":
    main()
