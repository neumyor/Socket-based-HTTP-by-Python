import json
import socket
import util
from router import router

USER = {}

socket = socket.socket()
socket.bind(('0.0.0.0', 80))
socket.listen(5)

while True:
    req, addr = socket.accept()
    print(f'接收到来自{addr[0]}:{addr[1]}的请求')

    req_info, req_header, req_data = util.handle(req)

    print(req_info)

    req_type, req_params, req_version = req_info.split()

    if req_type == 'GET':
        file_path = router[req_params]
        resp = util.pack(file_path, req_version)
        req.send(resp)
        req.close()
    elif req_type == 'POST':
        action = req_params
        if action == '/login':
            res = util.parseWebKitFormData(req_data)

            if res['username'] in USER and USER[res['username']] == res['password']:
                print("login success")
                resp = {
                    'token': 10086
                }
                req.send(json.dumps(resp).encode())
                req.close()
            else:
                print("login fail")
                req.send(b'HTTP/1.1 401 Unauthorized\r\n')
                req.close()
        elif action == '/register':
            res = util.parseWebKitFormData(req_data)

            USER[res['username']] = res['password']
            req.send(b'HTTP/1.1 200 Ok\r\n')
            print("register success", USER)
            req.close()
