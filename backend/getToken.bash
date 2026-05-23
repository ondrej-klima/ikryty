# --- Configuration Variables ---
KEYCLOAK_URL="https://civildefense.fit.vutbr.cz:8443"
REALM="myrealm"
CLIENT_ID="account" # The client ID you enabled the grant for
USERNAME="ondra" # The user's username
PASSWORD="r8AbuAbu" # The user's password

# --- 1. Get the Access Token ---
# This command sends the credentials to the token endpoint and uses jq to extract
# the access_token from the JSON response.
ACCESS_TOKEN=$(curl -s -X POST \
  "$KEYCLOAK_URL/realms/$REALM/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME" \
  -d "password=$PASSWORD" \
  -d "client_id=$CLIENT_ID" \
  -d "grant_type=password" | jq -r ".access_token")

# Check if we got a token
if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" == "null" ]; then
  echo "Failed to get access token. Check credentials and Keycloak client configuration."
  exit 1
fi

echo "Successfully obtained Access Token!"
# echo $ACCESS_TOKEN # Uncomment to see the token

# --- 2. Use the Token to Access the Protected API ---
echo -e "\n--- Calling Protected Python API ---"
curl -X GET http://civildefense.fit.vutbr.cz:8000/user_shelters \
  -H "Authorization: Bearer $ACCESS_TOKEN"

echo -e "\n"