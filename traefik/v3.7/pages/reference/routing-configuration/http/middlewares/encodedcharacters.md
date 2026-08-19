---
title: "Traefik EncodedCharacters Documentation"
description: "In Traefik Proxy, the EncodedCharacters middleware controls which ambiguous reserved encoded characters are allowed in the request path. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / EncodedCharacters"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/encodedcharacters.md"
source_url: "https://github.com/traefik/traefik/blob/faa1eb590646aed94e561e24a59be0c47353ae95/docs/content/reference/routing-configuration/http/middlewares/encodedcharacters.md"
---

The EncodedCharacters middleware controls which ambiguous reserved encoded characters are allowed in the request path.

When you use this middleware, by default, potentially dangerous encoded characters are rejected for security enhancement.

## Configuration Examples

**Docker & Swarm**

```yaml
# Allow encoded slash in the request path.
labels:
  - "traefik.http.middlewares.test-encodedchars.encodedcharacters.allowencodedslash=true"
```

**Kubernetes**

```yaml
# Allow encoded slash in the request path.
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-encodedchars
spec:
  encodedCharacters:
    allowEncodedSlash: true
```

**Consul Catalog**

```yaml
# Allow encoded slash in the request path.
- "traefik.http.middlewares.test-encodedchars.encodedcharacters.allowencodedslash=true"
```

**File (YAML)**

```yaml
# Allow encoded slash in the request path.
http:
  middlewares:
    test-encodedchars:
      encodedCharacters:
        allowEncodedSlash: true
```

**File (TOML)**

```toml
# Allow encoded slash in the request path.
[http.middlewares]
  [http.middlewares.test-encodedchars.encodedCharacters]
    allowEncodedSlash = true
```

## Configuration Options

When you are configuring these options, check if your backend is fully compliant with [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).
This helps avoid split-view situation, where Traefik and your backend interpret the same URL differently.

| Field                   | Description                                                        | Default | Required |
|-------------------------|--------------------------------------------------------------------|---------| -------- |
| <a id="opt-allowEncodedSlash" href="#opt-allowEncodedSlash" title="#opt-allowEncodedSlash">`allowEncodedSlash`</a> | Allow encoded slash (`%2F` and `%2f`) in the request path.         | `false` | No |
| <a id="opt-allowEncodedBackSlash" href="#opt-allowEncodedBackSlash" title="#opt-allowEncodedBackSlash">`allowEncodedBackSlash`</a> | Allow encoded backslash (`%5C` and `%5c`) in the request path.     | `false` | No |
| <a id="opt-allowEncodedSemicolon" href="#opt-allowEncodedSemicolon" title="#opt-allowEncodedSemicolon">`allowEncodedSemicolon`</a> | Allow encoded semicolon (`%3B` and `%3b`) in the request path.     | `false` | No |
| <a id="opt-allowEncodedPercent" href="#opt-allowEncodedPercent" title="#opt-allowEncodedPercent">`allowEncodedPercent`</a> | Allow encoded percent (`%25`) in the request path.                 | `false` | No |
| <a id="opt-allowEncodedQuestionMark" href="#opt-allowEncodedQuestionMark" title="#opt-allowEncodedQuestionMark">`allowEncodedQuestionMark`</a> | Allow encoded question mark (`%3F` and `%3f`) in the request path. | `false` | No |
| <a id="opt-allowEncodedHash" href="#opt-allowEncodedHash" title="#opt-allowEncodedHash">`allowEncodedHash`</a> | Allow encoded hash (`%23`) in the request path. | `false` | No |
