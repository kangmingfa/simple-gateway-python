"""
Gateway 服务：接收客户端请求，转发到后端 LLM 服务。
上游地址通过环境变量 LLM_BACKEND_URL 配置，默认 http://localhost:8000
"""

import os
import logging

import requests
from flask import Flask, Response, request
from requests.adapters import HTTPAdapter


# 1. 创建一个标准的 StreamHandler（负责把日志往控制台屏幕上抛）
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

# 2. 找到 urllib3 的根 Logger
urllib3_logger = logging.getLogger('urllib3')

# 3. 强制将它的级别调整为 DEBUG，并绑定处理器
urllib3_logger.setLevel(logging.DEBUG)
urllib3_logger.addHandler(console_handler)

app = Flask(__name__)

LLM_MODEL1_CLUSTER_URL = 'http://model1:1111'

# 使用 Session + HTTPAdapter 实现连接池复用，提升转发性能
session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=0)
# session.mount('http://', adapter)
# session.mount('https://', adapter)
session.mount('http://', adapter)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def proxy(path):
    """将请求原样转发到后端 LLM 服务，并返回响应。"""
    # 拼接上游 URL
    url = f"{LLM_MODEL1_CLUSTER_URL.rstrip('/')}/{path}"
    if request.query_string:
        url = f"{url}?{request.query_string.decode()}"

    # 过滤掉 Hop-by-hop 头，避免转发冲突
    excluded_headers = {
        'host', 'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade',
    }
    headers = {
        k: v for k, v in request.headers if k.lower() not in excluded_headers
    }
    headers['server_idx'] = request.headers.get('server-idx', '1')

    # 转发请求（通过 HTTPAdapter 管理的连接池）
    resp = session.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    # 构建响应头，排除不合适的头
    response_excluded = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
    response_headers = [
        (k, v) for k, v in resp.raw.headers.items()
        if k.lower() not in response_excluded
    ]

    return Response(resp.content, status=resp.status_code, headers=response_headers)


if __name__ == '__main__':
    port = int(os.environ.get('GATEWAY_PORT', 9000))
    app.run(host='0.0.0.0', port=port)
