from requests import get, post
from requests_toolbelt import MultipartEncoder
import json

FOLDER_ACCESS_SUFFIX='cSJe2JgtFFBwRuTKAJK6baNGUn0'

def get_app_access_token(app_id, app_secret, typ='tenant'):
    url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
        if typ=='tenant' else 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers={
        'Content-Type': 'application/json; charset=utf-8'
    }
    data=json.dumps({
        'app_id': app_id,
        'app_secret': app_secret
    })
    try:
        ret = post(url, headers=headers, data=data)
        ret = json.loads(ret.text)
        if ret['code'] == 0:
            token = ret[typ + '_access_token']
            print('App token got:', token)
            return token
        else:
            error_msg='Network Error:'+ret['msg']
            raise RuntimeError(error_msg)
    except Exception as e:
        print(e)
        raise e

def get_user_access_token(app_id, app_secret):
    app_access_token = get_app_access_token(app_id, app_secret, typ='app')
    headers={
        'Authorization': 'Bearer ' + app_access_token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    raise NotImplementedError

if __name__ == '__main__':
    app_id='cli_a525543dd1b8900b'
    app_secret='FMx2LKiCS5opyhGzGQkNYfbrpIUzdCgA'
    get_app_access_token(app_id, app_secret)