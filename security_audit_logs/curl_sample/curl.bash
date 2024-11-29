# curl should be installed for this to be used

# The URL for graph API
BASE_URL="https://graph.work.meta.com/"

# Add your app id and app secret proof from admin center here
APP_ID="YOUR_APP_ID"
APP_SECRET_PROOF="YOUR_APP_SECRET_PROOF"

# Fetch access token
RESPONSE=$(curl -s -F "access_token=$APP_ID|$APP_SECRET_PROOF" -F "grant_type=client_credentials" "$BASE_URL/work_get_token")
ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')

# Fetch security logs and save it to security_logs.csv
echo "timestamp,event_id,event,ip_address,useragent,target_username,actor_username,extra_data_summary" > security_logs.csv
curl --header "Authorization: Bearer $ACCESS_TOKEN" "$BASE_URL/security_audit_logs" |
  jq -r '.data[] | [.timestamp, .event_id, .event, .ip_address, .useragent, .target_username, .actor_username, .extra_data.summary] | @csv' >> security_logs.csv
