---
title: "Headers with Underscores"
description: "Learn how Traefik handles request headers with underscores to prevent header spoofing against backends that treat underscores and dashes identically. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Security / Headers with Underscores"
traefik_version: "v3.7"
upstream_path: "docs/content/security/header-underscores.md"
source_url: "https://github.com/traefik/traefik/blob/473e27980fe40f447ada70783ae28aabae86107d/docs/content/security/header-underscores.md"
---

# Headers with Underscores

Preventing Header Spoofing Through Underscore Variants

Underscores are valid characters in HTTP header names, but Go canonicalizes header names only on dashes.
As a result, a middleware managing a header in its dash form (e.g. `X-Auth-User` set by the ForwardAuth `authResponseHeaders` option)
does not see, and therefore cannot overwrite or remove, an underscore variant of that header (e.g. `X_Auth_User`).

Many backends map both forms to the same variable (CGI, WSGI, PHP, NGINX, ...): for them, `X-Auth-User` and `X_Auth_User`
are the same header. Against such a backend, a client can smuggle the underscore variant past a middleware that only manages
the dash form, and have the backend read the spoofed value, bypassing the protection the middleware was meant to provide.

## Configuration

The [`underscoreHeadersStrategy`](../reference/install-configuration/entrypoints.md#opt-http-underscoreHeadersStrategy) entry point option controls how request
headers with underscores in their names are handled before routing:

- `keep` (default): request headers with underscores are forwarded as is.
- `delete`: any request header whose name contains an underscore character is silently removed from the request.
- `reject`: any request carrying a header whose name contains an underscore character is rejected with a `400 Bad Request` response.

> **Warning — Security Considerations**
>
> When an entry point fronts a backend that interprets underscores and dashes in header names identically,
> keeping the default `keep` strategy is not recommended, as it leaves the backend open to the header spoofing described above.
> Set `underscoreHeadersStrategy` to `delete` or `reject` on such entry points.

**File (YAML)**

```yaml
entryPoints:
  websecure:
    address: ":443"
    http:
      underscoreHeadersStrategy: delete  # Default: keep
```

**File (TOML)**

```toml
[entryPoints.websecure]
  address = ":443"

  [entryPoints.websecure.http]
    underscoreHeadersStrategy = "delete"
```

**CLI**

```bash
--entryPoints.websecure.address=:443
--entryPoints.websecure.http.underscoreHeadersStrategy=delete
```
