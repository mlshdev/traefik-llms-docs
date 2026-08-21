---
title: "Nomad Service Discovery"
description: "Learn how to use Nomad as a provider for configuration discovery in Traefik Proxy. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Install Configuration / Configuration Discovery / Hashicorp / Nomad"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/providers/hashicorp/nomad.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/reference/install-configuration/providers/hashicorp/nomad.md"
---

# Traefik & Nomad Service Discovery

## Configuration Example

You can enable the Nomad provider with as detailed below:

**File (YAML)**

```yaml
providers:
  nomad: {}
```

**File (TOML)**

```toml
[providers.nomad]
```

**CLI**

```bash
--providers.nomad=true
```

Attaching tags to services:

```json
...
service {
  name = "myService"
  tags = [
    "traefik.http.routers.my-router.rule=Host(`example.com`)",
  ]
}
...
```

## Configuration Options

| Field | Description                                               | Default              | Required |
|:------|:----------------------------------------------------------|:---------------------|:---------|
| <a id="opt-providers-providersThrottleDuration" href="#opt-providers-providersThrottleDuration" title="#opt-providers-providersThrottleDuration">`providers.providersThrottleDuration`</a> | Minimum amount of time to wait for, after a configuration reload, before taking into account any new configuration refresh event.<br />If multiple events occur within this time, only the most recent one is taken into account, and all others are discarded.<br />**This option cannot be set per provider, but the throttling algorithm applies to each of them independently.** | 2s  | No |
| <a id="opt-providers-nomad-namespaces" href="#opt-providers-nomad-namespaces" title="#opt-providers-nomad-namespaces">`providers.nomad.namespaces`</a> | Defines the namespaces in which the nomad services will be discovered.|  ""     | No   |
| <a id="opt-providers-nomad-refreshInterval" href="#opt-providers-nomad-refreshInterval" title="#opt-providers-nomad-refreshInterval">`providers.nomad.refreshInterval`</a> | Defines the polling interval. This option is ignored when the `watch` option is enabled |  15s     | No   |
| <a id="opt-providers-nomad-watch" href="#opt-providers-nomad-watch" title="#opt-providers-nomad-watch">`providers.nomad.watch`</a> | Enables the watch mode to refresh the configuration on a per-event basis. |  false     | No   |
| <a id="opt-providers-nomad-throttleDuration" href="#opt-providers-nomad-throttleDuration" title="#opt-providers-nomad-throttleDuration">`providers.nomad.throttleDuration`</a> | Defines how often the provider is allowed to handle service events from Nomad. This option is only compatible when the `watch` option is enabled |  0s     | No   |
| <a id="opt-providers-nomad-defaultRule" href="#opt-providers-nomad-defaultRule" title="#opt-providers-nomad-defaultRule">`providers.nomad.defaultRule`</a> | The Default Host rule for all services. See [here](#defaultrule) for more information |   ```"Host(`{{ normalize .Name }}`)"```   | No   |
| <a id="opt-providers-nomad-constraints" href="#opt-providers-nomad-constraints" title="#opt-providers-nomad-constraints">`providers.nomad.constraints`</a> | Defines an expression that Traefik matches against the container labels to determine whether to create any route for that container. See [here](#constraints) for more information.  |  ""   | No   |
| <a id="opt-providers-nomad-exposedByDefault" href="#opt-providers-nomad-exposedByDefault" title="#opt-providers-nomad-exposedByDefault">`providers.nomad.exposedByDefault`</a> | Expose Nomad services by default in Traefik. If set to `false`, services that do not have a `traefik.enable=true` tag will be ignored from the resulting routing configuration. See [here](../overview.md#exposedbydefault-and-traefikenable) for additional information |  true    | No   |
| <a id="opt-providers-nomad-allowEmptyServices" href="#opt-providers-nomad-allowEmptyServices" title="#opt-providers-nomad-allowEmptyServices">`providers.nomad.allowEmptyServices`</a> |  Instructs the provider to create any [servers load balancer](../../../../reference/routing-configuration/http/load-balancing/service.md#service-load-balancer) defined for Nomad services even when those services are scaled to zero instances. |  false   | No   |
| <a id="opt-providers-nomad-prefix" href="#opt-providers-nomad-prefix" title="#opt-providers-nomad-prefix">`providers.nomad.prefix`</a> | Defines the prefix for Nomad service tags defining Traefik labels. | `traefik`     | No   |
| <a id="opt-providers-nomad-stale" href="#opt-providers-nomad-stale" title="#opt-providers-nomad-stale">`providers.nomad.stale`</a> | Instructs Traefik to use stale consistency for Nomad service API reads. See [here](#stale) for more information | false   | No   |
| <a id="opt-providers-nomad-endpoint-address" href="#opt-providers-nomad-endpoint-address" title="#opt-providers-nomad-endpoint-address">`providers.nomad.endpoint.address`</a> | Defines the Address of the Nomad server. | `http://127.0.0.1:4646`  | No   |
| <a id="opt-providers-nomad-endpoint-region" href="#opt-providers-nomad-endpoint-region" title="#opt-providers-nomad-endpoint-region">`providers.nomad.endpoint.region`</a> | Defines the Nomad region to use. If not provided, the local agent region is used. | ""  | No   |
| <a id="opt-providers-nomad-endpoint-token" href="#opt-providers-nomad-endpoint-token" title="#opt-providers-nomad-endpoint-token">`providers.nomad.endpoint.token`</a> | Defines a per-request ACL token if Nomad ACLs are enabled. See [here](#token) for more information | ""  | No   |
| <a id="opt-providers-nomad-endpoint-endpointWaitTime" href="#opt-providers-nomad-endpoint-endpointWaitTime" title="#opt-providers-nomad-endpoint-endpointWaitTime">`providers.nomad.endpoint.endpointWaitTime`</a> | Defines a duration for which a `watch` can block. If not provided, the agent default values will be used. | ""  | No   |
| <a id="opt-providers-nomad-endpoint-tls" href="#opt-providers-nomad-endpoint-tls" title="#opt-providers-nomad-endpoint-tls">`providers.nomad.endpoint.tls`</a> | Defines the TLS configuration used for the secure connection to the Nomad APi.  |  -   | No   |
| <a id="opt-providers-nomad-endpoint-tls-ca" href="#opt-providers-nomad-endpoint-tls-ca" title="#opt-providers-nomad-endpoint-tls-ca">`providers.nomad.endpoint.tls.ca`</a> | Defines the path to the certificate authority used for the secure connection to the Nomad API, it defaults to the system bundle.  |   ""  | No   |
| <a id="opt-providers-nomad-endpoint-tls-cert" href="#opt-providers-nomad-endpoint-tls-cert" title="#opt-providers-nomad-endpoint-tls-cert">`providers.nomad.endpoint.tls.cert`</a> | Defines the path to the public certificate used for the secure connection to the Nomad API. When using this option, setting the `key` option is required. | '"  | Yes   |
| <a id="opt-providers-nomad-endpoint-tls-key" href="#opt-providers-nomad-endpoint-tls-key" title="#opt-providers-nomad-endpoint-tls-key">`providers.nomad.endpoint.tls.key`</a> | Defines the path to the private key used for the secure connection to the Nomad API. When using this option, setting the `cert` option is required. |  ""   | Yes   |
| <a id="opt-providers-nomad-endpoint-tls-insecureSkipVerify" href="#opt-providers-nomad-endpoint-tls-insecureSkipVerify" title="#opt-providers-nomad-endpoint-tls-insecureSkipVerify">`providers.nomad.endpoint.tls.insecureSkipVerify`</a> | Instructs the provider to accept any certificate presented by Nomad when establishing a TLS connection, regardless of the hostnames the certificate covers. | false   | No   |

### `namespaces`

The `namespaces` option defines the namespaces in which the nomad services will be discovered.
When using the `namespaces` option, the discovered object names will be suffixed as shown below:

```text
<resource-name>@nomad-<namespace>
```

> **Warning**
>
> One should only define either the `namespaces` option or the `namespace` option.

**File (YAML)**

```yaml
providers:
  nomad:
    namespaces:
      - "ns1"
      - "ns2"
    # ...
```

**File (TOML)**

```toml
[providers.nomad]
  namespaces = ["ns1", "ns2"]
  # ...
```

**CLI**

```bash
--providers.nomad.namespaces=ns1,ns2
# ...
```

### `stale`

Use stale consistency for Nomad service API reads.

> **Note**
>
> This makes reads very fast and scalable at the cost of a higher likelihood of stale values.
>
> For more information, see the Nomad [documentation on consistency](https://www.nomadproject.io/api-docs#consistency-modes).

**File (YAML)**

```yaml
providers:
  nomad:
    stale: true
    # ...
```

**File (TOML)**

```toml
[providers.nomad]
  stale = true
  # ...
```

**CLI**

```bash
--providers.nomad.stale=true
# ...
```

### `token`

Token is used to provide a per-request ACL token, if Nomad ACLs are enabled.
The appropriate ACL privilege for this token is 'read-job', as outlined in the [Nomad documentation on ACL](https://developer.hashicorp.com/nomad/tutorials/access-control/access-control-policies).

**File (YAML)**

```yaml
providers:
  nomad:
    endpoint:
      token: test
    # ...
```

**File (TOML)**

```toml
[providers.nomad]
  [providers.nomad.endpoint]
    token = "test"
    # ...
```

**CLI**

```bash
--providers.nomad.endpoint.token=test
# ...
```

### `defaultRule`

The default host rule for all services.

For a given service, if no routing rule was defined by a tag, it is defined by this `defaultRule` instead.
The `defaultRule` must be set to a valid [Go template](https://pkg.go.dev/text/template/),
and can include [sprig template functions](https://masterminds.github.io/sprig/).
The service name can be accessed with the `Name` identifier,
and the template has access to all the labels (i.e. tags beginning with the `prefix`) defined on this service.

The option can be overridden on an instance basis with the `traefik.http.routers.{name-of-your-choice}.rule` tag.

**File (YAML)**

```yaml
providers:
  nomad:
    defaultRule: "Host(`{{ .Name }}.{{ index .Labels \"customLabel\"}}`)"
    # ...
```

**File (TOML)**

```toml
[providers.nomad]
  defaultRule = "Host(`{{ .Name }}.{{ index .Labels \"customLabel\"}}`)"
  # ...
```

**CLI**

```bash
--providers.nomad.defaultRule='Host(`{{ .Name }}.{{ index .Labels "customLabel"}}`)'
# ...
```

> **Info — Default rule and Traefik service**
>
> The exposure of the Traefik container, combined with the default rule mechanism,
> can lead to create a router targeting itself in a loop.
> In this case, to prevent an infinite loop,
> Traefik adds an internal middleware to refuse the request if it comes from the same router.

### `constraints`

The `constraints` option can be set to an expression that Traefik matches against the service tags to determine whether
to create any route for that service. If none of the service tags match the expression, no route for that service is
created. If the expression is empty, all detected services are included.

The expression syntax is based on the ```Tag(`tag`)```, and ```TagRegex(`tag`)``` functions,
as well as the usual boolean logic, as shown in examples below.

> **Tip — Constraints key limitations**
>
> Note that `traefik.*` is a reserved label namespace for configuration and can not be used as a key for custom constraints.

> **Example — Constraints Expression Examples**
>
> ```toml
> # Includes only services having the tag `a.tag.name=foo`
> constraints = "Tag(`a.tag.name=foo`)"
> ```
>
> ```toml
> # Excludes services having any tag `a.tag.name=foo`
> constraints = "!Tag(`a.tag.name=foo`)"
> ```
>
> ```toml
> # With logical AND.
> constraints = "Tag(`a.tag.name`) && Tag(`another.tag.name`)"
> ```
>
> ```toml
> # With logical OR.
> constraints = "Tag(`a.tag.name`) || Tag(`another.tag.name`)"
> ```
>
> ```toml
> # With logical AND and OR, with precedence set by parentheses.
> constraints = "Tag(`a.tag.name`) && (Tag(`another.tag.name`) || Tag(`yet.another.tag.name`))"
> ```
>
> ```toml
> # Includes only services having a tag matching the `a\.tag\.t.+` regular expression.
> constraints = "TagRegex(`a\.tag\.t.+`)"
> ```

**File (YAML)**

```yaml
providers:
  nomad:
    constraints: "Tag(`a.tag.name`)"
    # ...
```

**File (TOML)**

```toml
[providers.nomad]
  constraints = "Tag(`a.tag.name`)"
  # ...
```

**CLI**

```bash
--providers.nomad.constraints="Tag(`a.tag.name`)"
# ...
```

For additional information, refer to [Restrict the Scope of Service Discovery](../overview.md#exposedbydefault-and-traefikenable).

## Routing Configuration

See the dedicated section in [routing](../../../../reference/routing-configuration/other-providers/nomad.md).
