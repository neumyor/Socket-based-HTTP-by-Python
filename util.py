import os


def handle(req):
    file = req.makefile('rb')

    req_line = file.readline().decode()
    req_header = {}
    while True:
        raw_req_header_line = file.readline().decode().replace('\r\n', '')
        spl_list = raw_req_header_line.split(':', 1)

        if len(spl_list) == 1:
            break

        key, value = spl_list
        req_header[key] = value

    req_data = ''
    if 'Content-Length' in req_header:
        req_data = file.read(int(req_header['Content-Length'])).decode()

    return req_line, req_header, req_data


def pack(resp_path, req_version, content=None):
    resp_type = os.path.splitext(resp_path)[-1]

    if resp_type == '.html':
        content_type = 'text/html;charset=utf-8'
    elif resp_type == '.ico':
        content_type = 'image/webp'

    true_resp = b''
    true_resp += f'{req_version} 200 OK\r\n'.encode()
    true_resp += f'content-type: {content_type}\r\n'.encode()
    true_resp += b'\r\n'

    with open(resp_path, 'rb') as f:
        if content:
            tmp = f.read().replace(b'{CONTENT}', content.encode())
        else:
            tmp = f.read()
        true_resp += tmp
    return true_resp


def parseWebKitFormData(raw_data):
    import re
    ret = {}
    cols = raw_data.split('------')
    for col in cols:
        search_res = re.search(r'name="(.*)"[\r\n ]*(.*)[\r\n ]*', col)
        if search_res is None:
            continue
        key = search_res.group(1).replace('\r', '').replace('\n', '')
        value = search_res.group(2).replace('\r', '').replace('\n', '')
        ret[key] = value

    return ret
