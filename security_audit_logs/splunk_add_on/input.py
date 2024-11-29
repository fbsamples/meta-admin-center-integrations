# encoding = utf-8

import json
import time

"""
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
"""
"""
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
"""


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    pass


def collect_events(helper, ew):

    helper.set_log_level("info")

    base_url = "https://graph.work.meta.com/"
    access_token = get_access_token(helper, ew, base_url)

    security_logs_endpoint = "security_audit_logs"
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    parameters = {"limit": "1000"}

    security_logs = []

    should_get_logs = True

    while should_get_logs is True:
        response = helper.send_http_request(
            base_url + security_logs_endpoint,
            "GET",
            parameters=parameters,
            payload=None,
            headers=headers,
            cookies=None,
            verify=True,
            cert=None,
            timeout=None,
            use_proxy=True,
        )
        response.raise_for_status()

        r_json = response.json()
        data = r_json["data"]

        for log in data:
            state = helper.get_check_point(str(log["id"]))
            if state is None:
                security_logs.append(log)
                helper.save_check_point(str(log["id"]), "Indexed")
            # Uncomment line below to delete the saved security logs data (check point).
            # helper.delete_check_point(str(log["id"]))

        if r_json.get("paging") is None:
            should_get_logs = False
        else:
            parameters["after"] = r_json["paging"]["cursors"]["after"]

    for security_log in security_logs:
        event = helper.new_event(
            data=json.dumps(security_log),
            time=None,
            host=None,
            index=None,
            source=None,
            sourcetype=None,
            done=True,
            unbroken=True,
        )
        ew.write_event(event)


def get_access_token(helper, ew, base_url):
    opt_app_id = helper.get_arg("app_id")
    opt_app_secret = helper.get_arg("app_secret")

    access_token_endpoint = "work_get_token"
    current_timestamp = time.time()

    access_token_time = helper.get_check_point("access_token_time")
    access_token = None

    if access_token_time is not None and float(access_token_time) > current_timestamp:
        # return saved access token
        access_token = helper.get_check_point("access_token")

    if access_token is None:
        parameters = {
            "access_token": opt_app_id + "|" + opt_app_secret,
            "grant_type": "client_credentials",
        }

        response = helper.send_http_request(
            base_url + access_token_endpoint,
            "POST",
            parameters=parameters,
            payload=None,
            headers=None,
            cookies=None,
            verify=True,
            cert=None,
            timeout=None,
            use_proxy=True,
        )

        r_json = response.json()

        # check the response status, if the status is not sucessful, raise requests.HTTPError
        response.raise_for_status()

        access_token = r_json["access_token"]
        helper.save_check_point("access_token", access_token)

        # Expiry time of access token is 2 hours.
        ts = time.time() + 2 * 60 * 60
        helper.save_check_point("access_token_time", str(ts))

    return access_token
