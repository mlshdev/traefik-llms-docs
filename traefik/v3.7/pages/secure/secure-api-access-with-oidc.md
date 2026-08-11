---
title: "Secure API Access with OIDC"
description: "Traefik Hub API Gateway - The OIDC Authentication middleware secures your applications by delegating the authentication to an external provider."
section: "Secure"
breadcrumb: "Secure / Secure Access with OIDC"
traefik_version: "v3.7"
upstream_path: "docs/content/secure/secure-api-access-with-oidc.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/secure/secure-api-access-with-oidc.md"
---

# Secure API Access with OIDC

> **Info — Traefik Hub Feature**
>
> This middleware is available exclusively in [Traefik Hub](https://traefik.io/traefik-hub/). Learn more about [Traefik Hub's advanced features](https://doc.traefik.io/traefik-hub/api-gateway/intro).

OpenID Connect Authentication is built on top of the OAuth2 Authorization Code Flow (defined in [OAuth 2.0 RFC 6749, section 4.1](https://tools.ietf.org/html/rfc6749#section-4.1)).
It allows an application to be secured by delegating authentication to an external provider (Keycloak, Okta etc.)
and obtaining the end user's session claims and scopes for authorization purposes.

To authenticate the user, the middleware redirects through the authentication provider.
Once the authentication is complete, users are redirected back to the middleware before being authorized to access the upstream application, as described in the diagram below:

![OpenID Connect authentication flow](https://raw.githubusercontent.com/traefik/traefik/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/assets/img/secure/oidc-auth-flow.png)

<br />

To allow the OIDC Middleware to use the credentials provided by the requests, apply the following configuration:

**Middleware OIDC**

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: oidc-login
  namespace: apps
spec:
  plugin:
    oidc:
      issuer: MY_ISSUER_URL
      clientId: "urn:k8s:secret:oidc-client:client_id"
      clientSecret: "urn:k8s:secret:oidc-client:client_secret"
      redirectUrl: /oidc/callback
```

**Kubernetes Secrets**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: oidc-client
stringData:
  client_id: my-oauth-client-ID # Set your ClientID here
  client_secret: my-oauth-client-secret # Set your client secret here
```

**IngressRoute**

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: secure-applications-apigateway-oauth2-client-credentials
  namespace: apps
spec:
  entryPoints:
    - websecure
  routes:
  - match: Path(`/my-app`)
    kind: Rule
    services:
    - name: whoami
      port: 80
    middlewares:
    - name: oidc-login
```

**Service & Deployment**

```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: whoami
  namespace: apps
spec:
  replicas: 3
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
      - name: whoami
        image: traefik/whoami

---
apiVersion: v1
kind: Service
metadata:
  name: whoami
  namespace: apps
spec:
  ports:
  - port: 80
    name: whoami
  selector:
    app: whoami
```

> **Note — Advanced Configuration**
>
> Advanced options are described in the [reference page](../reference/routing-configuration/http/middlewares/oidc.md).
>
> For example, you can find how to customize the session storage:
> - Using a cookie ([Options `session`](../reference/routing-configuration/http/middlewares/oidc.md#configuration-options) (default behavior))
> - Using a [Redis store](../reference/routing-configuration/http/middlewares/oidc.md#sessionstore).

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
