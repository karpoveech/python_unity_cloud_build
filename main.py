from __future__ import absolute_import, unicode_literals
import requests
import creds


def get_url(func_name, extend=None):
    auth_base = f"orgs/{creds.ORGID}/projects/{creds.PROJECTS}/buildtargets/{creds.BUILD_TARGETS}"
    if extend:
        url_base = "https://build-api.cloud.unity3d.com/api/v1/{auth}/{func}{extend}"
        return url_base.format(auth=auth_base, func=func_name, extend=extend)

    else:
        url_base = "https://build-api.cloud.unity3d.com/api/v1/{auth}/{func}"
        return url_base.format(auth=auth_base, func=func_name)


def get_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": "Basic {token}".format(token=creds.API_TOKEN),
    }


def execute_build():
    response = requests.post(get_url("builds"), headers=get_headers())
    print(response.text), response.status_code
    return


if __name__ == "__main__":
    execute_build()
