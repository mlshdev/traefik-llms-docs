---
title: "Traefik RedirectRegex Documentation"
description: "In Traefik Proxy's HTTP middleware, RedirectRegex redirecting clients to different locations. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / Middlewares / RedirectRegex"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/middlewares/redirectregex.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/routing-configuration/http/middlewares/redirectregex.md"
---

The `RedirectRegex` redirects a request using regex matching and replacement.

## Configuration Examples

**Structured (YAML)**

```yaml
# Redirect with domain replacement
http:
  middlewares:
    test-redirectregex:
      redirectRegex:
        regex: "^http://localhost/(.*)"
        replacement: "http://mydomain/${1}"
```

**Structured (TOML)**

```toml
# Redirect with domain replacement
[http.middlewares]
  [http.middlewares.test-redirectregex.redirectRegex]
    regex = "^http://localhost/(.*)"
    replacement = "http://mydomain/${1}"
```

**Labels**

```yaml
# Redirect with domain replacement
# Note: all dollar signs need to be doubled for escaping.
labels:
  - "traefik.http.middlewares.test-redirectregex.redirectregex.regex=^http://localhost/(.*)"
  - "traefik.http.middlewares.test-redirectregex.redirectregex.replacement=http://mydomain/$${1}"
```

**Tags**

```json
// Redirect with domain replacement
// Note: all dollar signs need to be doubled for escaping.
{
  // ...
  "Tags" : [
    "traefik.http.middlewares.test-redirectregex.redirectregex.regex=^http://localhost/(.*)"
    "traefik.http.middlewares.test-redirectregex.redirectregex.replacement=http://mydomain/$${1}"
  ]
}
```

**Kubernetes**

```yaml
# Redirect with domain replacement
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: test-redirectregex
spec:
  redirectRegex:
    regex: ^http://localhost/(.*)
    replacement: http://mydomain/${1}
```

## Configuration Options

<!-- markdownlint-disable MD013 -->

| Field                        | Description                                                                                                                                                                                                | Default | Required |
|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-regex" href="#opt-regex" title="#opt-regex">`regex`</a> | The `regex` option is the regular expression to match and capture elements from the request URL.| "" | Yes |
| <a id="opt-permanent" href="#opt-permanent" title="#opt-permanent">`permanent`</a> | Enable a permanent redirection. | false | No |
| <a id="opt-replacement" href="#opt-replacement" title="#opt-replacement">`replacement`</a> | The `replacement` option defines how to modify the URL to have the new target URL..<br /> `$1x` is equivalent to `${1x}`, not `${1}x` (see [Regexp.Expand](https://golang.org/pkg/regexp/#Regexp.Expand)), so use `${1}` syntax. | "" | No |

### `regex`

The `regex` option is the regular expression to match and capture elements from the request URL.

> **Tip**
>
> Regular expressions and replacements can be tested using online tools such as [Go Playground](https://play.golang.org/p/mWU9p-wk2ru) or the [Regex101](https://regex101.com/r/58sIgx/2).
>
> When defining a regular expression within YAML, any escaped character needs to be escaped twice: `example\.com` needs to be written as `example\\.com`.

### `replacement`

The `replacement` option defines how to modify the URL to have the new target URL.

> **Warning**
>
> Care should be taken when defining replacement expand variables: `$1x` is equivalent to `${1x}`, not `${1}x` (see [Regexp.Expand](https://golang.org/pkg/regexp/#Regexp.Expand)), so use `${1}` syntax.

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
