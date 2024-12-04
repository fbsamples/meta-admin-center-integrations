# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import csv
import json

import requests


def get_access_token(app_id, app_secret_proof, base_url):
    url = f"{base_url}/work_get_token"
    payload = {
        "access_token": f"{app_id}|{app_secret_proof}",
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=payload)
    return response.json().get("access_token")


def fetch_security_audit_logs(access_token, base_url):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{base_url}/security_audit_logs?limit=1000", headers=headers
    )

    if response.status_code == 200:
        while True:
            data = json.loads(response.text)
            write_security_logs_to_csv(data)
            paging = data.get("paging", {})
            cursor = paging.get("cursors", {})
            after = cursor.get("after")
            if not after:
                break
            response = requests.get(
                f"{base_url}/security_audit_logs?limit=1000&after={after}",
                headers=headers,
            )
    else:
        print(f"Failed to fetch logs: {response.status_code} - {response.text}")


def write_security_logs_to_csv(data):
    with open("security_logs.csv", "a", newline="") as csvfile:
        fieldnames = [
            "timestamp",
            "event_id",
            "event",
            "ip_address",
            "useragent",
            "target_username",
            "actor_username",
            "extra_data_summary",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()
        for item in data.get("data", []):
            writer.writerow(
                {
                    "timestamp": item.get("timestamp"),
                    "event_id": item.get("event_id"),
                    "event": item.get("event"),
                    "ip_address": item.get("ip_address"),
                    "useragent": item.get("useragent"),
                    "target_username": item.get("target_username"),
                    "actor_username": item.get("actor_username"),
                    "extra_data_summary": item.get("extra_data", {}).get("summary"),
                }
            )


# Example usage:
app_id = "YOUR_APP_ID"
app_secret_proof = "YOUR_APP_SECRET_PROOF"
base_url = "https://graph.work.meta.com/"

# Get access token
token_response = get_access_token(app_id, app_secret_proof, base_url)

# Get logs
fetch_security_audit_logs(token_response, base_url)
