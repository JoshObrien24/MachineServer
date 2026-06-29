import http.server
import socketserver
import json
import os
import socket
import cgi
import Machines.Machines as Machines
import Machines.MachineUtil as MachineUtil
import Server.ServerUtil as ServerUtil

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/machines":
            self.send_json(Machines.loadFromJsonRaw())
            return

        if self.path.startswith('/status/'):
            machine_id = int(self.path.split("/")[-1])
            self.send_json(MachineUtil.getStatus(machine_id))
            return

        if self.path == "/queue":
            self.send_json(ServerUtil.getQueue())
            return

        return super().do_GET()

    def do_POST(self):
        if self.path == "/upload":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"]
                }
            )

            if "file" not in form:
                self.send_error(400, "No file supplied")
                return

            file_item = form["file"]
            filename = os.path.basename(file_item.filename)
            if ServerUtil.verifyQueue(form['machineID'].value, filename):
                ServerUtil.addFileToQueue(form['machineID'].value, filename)
            else:
                self.send_error(401, "File Already Uploaded")

            with open(os.path.join("Server/Uploads", filename), "wb") as f:
                f.write(file_item.file.read())

            self.send_json({
                "success": True,
                "file": filename
            })

            return

        if self.path == "/add-machine":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            machine = json.loads(body)
            
            MachineUtil.addMachineJSON(machine)

            self.send_json({
                "success": True
            })
            
            return

        self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/machine/"):
            machine_id = int(self.path.split("/")[-1])
            MachineUtil.deleteMachineByID(machine_id)
            self.send_json({
                "success": True
            })
            return

        self.send_error(404)

def startServer() -> None:
    with socketserver.ThreadingTCPServer(("", PORT), RequestHandler) as httpd:
        ServerUtil.createQueueFile()
        print(f"Listening on port {PORT}")
        print(f"http://{socket.gethostbyname(socket.gethostname())}:{PORT}/Server/web/")

        httpd.serve_forever()