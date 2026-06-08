import http.server
import socketserver
import json
import os
import socket
import cgi
import Machines.Machines as Machines
import Machines.MachineUtil as MachineUtil

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
            MachineUtil.addFileToQueue(form['machineID'].value, filename)

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


with socketserver.ThreadingTCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Listening on port {PORT}")
    print(f"http://{socket.gethostbyname(socket.gethostname())}:{PORT}")

    httpd.serve_forever()