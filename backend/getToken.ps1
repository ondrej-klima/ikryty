# --- Configuration Variables ---
$keycloakUrl = "https://civildefense.fit.vutbr.cz:8443"
$realm = "myrealm"
$clientId = "account" # The client ID you enabled the grant for
$username = "ondra" # The user's username
$password = "r8AbuAbu" # The user's password

# IMPORTANT: If your Keycloak server uses a self-signed certificate, you might need this line to bypass TLS validation.
# For production, you should use properly signed certificates.
# [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# --- 1. Get the Access Token ---
Write-Host "Requesting Access Token from Keycloak..."

# The body of the POST request, structured as a PowerShell hashtable (dictionary)
$tokenRequestBody = @{
    username     = $username
    password     = $password
    client_id    = $clientId
    grant_type   = "password"
}

try {
    # Invoke-RestMethod automatically handles the request and parses the JSON response into a PowerShell object
    $tokenResponse = Invoke-RestMethod -Uri "$keycloakUrl/realms/$realm/protocol/openid-connect/token" -Method Post -Body $tokenRequestBody

    # Access the access_token property directly from the response object. No 'jq' needed!
    $accessToken = $tokenResponse.access_token

    if (-not $accessToken) {
        Write-Error "Failed to get access token. Response did not contain an access_token."
        # The script will stop here if it enters the 'catch' block or this 'if'
        return
    }

    Write-Host "Successfully obtained Access Token!"
    # Write-Host $accessToken # Uncomment to see the token

} catch {
    Write-Error "An error occurred while getting the token: $($_.Exception.Message)"
    # Exit the script on failure
    return
}


# --- 2. Use the Token to Access the Protected API ---
Write-Host "`n--- Calling Protected Python API ---"

# Create the headers hashtable for the API request
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

try {
    # Call your Python backend with the Authorization header
    $apiResponse = Invoke-RestMethod -Uri "http://localhost:8000/user_shelters" -Method Get -Headers $headers

    # The response is already a PowerShell object, you can format it nicely
    Write-Host "API Response:"
    $apiResponse | ConvertTo-Json

} catch {
    Write-Error "An error occurred while calling the API: $($_.Exception.Message)"
}

Write-Host ""