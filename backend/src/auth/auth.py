import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from functools import lru_cache
from fastapi.security import OAuth2AuthorizationCodeBearer

"""
Modul pro autentizaci a autorizaci uživatelů (Keycloak Integration).

Tento modul zajišťuje bezpečnostní vrstvu aplikace pomocí standardu OAuth2 a protokolu OpenID Connect.
Slouží primárně k validaci přístupových tokenů (JWT - JSON Web Tokens) vydaných externím
identitním serverem Keycloak.

Hlavní zodpovědnosti modulu:
----------------------------
1.  **Správa veřejných klíčů (JWKS):**
    Stahuje JSON Web Key Set z Keycloak serveru. Využívá LRU cache (`@lru_cache`)
    pro optimalizaci výkonu, aby se klíče nestahovaly při každém požadavku.

2.  **Validace tokenů:**
    Ověřuje kryptografický podpis tokenu, jeho platnost (expiraci), vydavatele (Issuer)
    a oprávněného příjemce (Audience).

3.  **Integrace do FastAPI:**
    Poskytuje asynchronní funkci `get_current_user`, která slouží jako "Dependency"
    pro endpointy. Tato funkce automaticky extrahuje token z hlavičky `Authorization`,
    ověří ho a vrátí payload (data uživatele) nebo vyvolá `HTTPException`.

Konfigurace:
------------
Modul vyžaduje správně nastavené konstanty pro URL Keycloaku, název realmu
a očekávanou 'audience' (klientské ID aplikace).

Příklad použití v routeru:
--------------------------
    @router.get("/protected-route")
    async def protected_route(current_user: dict = Depends(get_current_user)):
        return {"user": current_user['preferred_username']}
"""

# --- Configuration ---
KEYCLOAK_URL = "https://civildefense.fit.vutbr.cz:8443"
REALM_NAME = "ikryty"
API_AUDIENCE = "my-python-api"  # The 'Client ID' of your backend client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token")


# --- Caching for JWKS ---
# Use LRU cache to avoid fetching the JWKS on every single request.
# This will cache the result of the function call.
@lru_cache(maxsize=1)
def get_jwks():
    """
    Stáhne sadu veřejných klíčů (JWKS) z Keycloak serveru.

    Výsledek je cachován pomocí LRU cache (s pamětí pro 1 výsledek),
    aby se zamezilo opakovanému stahování klíčů při každém požadavku na API.

    Returns:
        dict: JSON odpověď obsahující veřejné klíče.

    Raises:
        HTTPException: Pokud se nepodaří spojit s Keycloak serverem (status 503).
    """
    try:
        response = requests.get(f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # This is a critical error, as the service cannot verify any tokens without the keys.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to Keycloak to fetch public keys: {e}",
        )


# --- Dependency for Token Validation ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Ověří platnost JWT tokenu a vrátí payload (data uživatele).
    Tato funkce slouží jako 'Dependency' pro endpointy FastAPI.

    Args:
        token (str): Bearer token získaný z hlavičky Authorization.

    Returns:
        dict: Dekódovaný payload tokenu obsahující informace o uživateli.

    Raises:
        HTTPException:
            - 401 Unauthorized: Pokud je token neplatný, expirovaný nebo chybí oprávnění.
            - 503 Service Unavailable: Pokud nelze získat klíče pro ověření.
            - 500 Internal Server Error: Při neočekávané chybě.
    """
    #print('get_current_user')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Get the public keys from Keycloak
        jwks = get_jwks()

        # 2. Get the unverified header from the token to find the Key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        token_kid = unverified_header.get("kid")

        if not token_kid:
            raise HTTPException(status_code=401, detail="Token is missing 'kid' in header")

        # 3. Find the correct public key from the JWKS
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == token_kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Signing key not found in JWKS")

        # 4. Decode and validate the token using the correct key
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=f"{KEYCLOAK_URL}/realms/{REALM_NAME}"
        )

        username: str = payload.get("preferred_username")
        if username is None:
            raise credentials_exception

        #print(payload.get("realm_access", {}).get("roles", []))
        return payload

    except JWTError as e:
        # This catches all JWT-related errors, e.g., signature expired, invalid signature, etc.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        # Re-raise HTTPExceptions to avoid them being caught by the generic except block
        raise e
    except Exception as e:
        # Catch any other unexpected errors during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during authentication: {e}"
        )
