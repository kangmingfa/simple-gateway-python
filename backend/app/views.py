import os

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def model_info(request):
    """
    返回当前服务的 server id 和模型名字。
    通过环境变量 SERVER_ID 和 MODEL_NAME 读取配置。
    """
    server_id = os.environ.get('SERVER_ID', 'unknown')
    model_name = os.environ.get('MODEL_NAME', 'unknown')

    return JsonResponse({
        'server_id': server_id,
        'model_name': model_name,
    })
