#Client-to-Cloud Security Guidelines

## 1. HTTPS Enforcement
- All communication must use HTTPS (TLS 1.2 or higher).
- HTTP must be disabled or redirected to HTTPS.

## 2. Authentication
- All API requests must include a Bearer Token in the `Authorization` header.
- No endpoints may be public unless explicitly stated.

## 3. Token Management
- Tokens must expire (e.g. 30–60 minutes).
- Token refresh must be planned (e.g. using refresh tokens).

## 4. Token Storage
- Web: HttpOnly cookies or memory (not localStorage).
- Mobile: Secure storage (Keychain/Keystore).

## 5. Data Protection
- No sensitive data in URLs or in plaintext.
- Use POST with body for all sensitive requests.

## 6. Notes
- Never hardcode secrets in the frontend.
- Plan for OAuth2 / OpenID Connect support.
