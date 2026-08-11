---
title: "Traefik TLS Certificates Documentation"
description: "Learn how to configure the transport layer security (TLS) connection in Traefik Proxy. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / HTTP / TLS / TLS Certificates"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/http/tls/tls-certificates.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/http/tls/tls-certificates.md"
---

> **Info**
>
> When a router has to handle HTTPS traffic, it should be specified with a `tls` field of the router definition.

## Certificates Definition

### Automated

See the [Let's Encrypt](../../../install-configuration/tls/certificate-resolvers/acme.md) page.

### User defined

To add / remove TLS certificates, even when Traefik is already running, their definition can be added to the [dynamic configuration](../../dynamic-configuration-methods.md#providing-dynamic-routing-configuration-to-traefik), in the `[[tls.certificates]]` section:

**Structured (YAML)**

```yaml
tls:
  certificates:
    - certFile: /path/to/domain.cert
      keyFile: /path/to/domain.key
    - certFile: /path/to/other-domain.cert
      keyFile: /path/to/other-domain.key
```

**Structured (TOML)**

```toml
[[tls.certificates]]
  certFile = "/path/to/domain.cert"
  keyFile = "/path/to/domain.key"

[[tls.certificates]]
  certFile = "/path/to/other-domain.cert"
  keyFile = "/path/to/other-domain.key"
```

> **Important — Restriction**
>
> In the above example, we've used the [file provider](../../../install-configuration/providers/others/file.md) to handle these definitions.
> It is the only available method to configure the certificates (as well as the options and the stores).
> However, in [Kubernetes](../../../install-configuration/providers/kubernetes/kubernetes-crd.md), the certificates can and must be provided by [secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

#### Certificate selection (SNI)

Traefik selects the certificate to present during the TLS handshake, based on the Server Name Indication (SNI) sent by the client.

However, HTTP router rules (e.g., `Host()`) are evaluated after TLS has been established, so they do not influence certificate selection.

##### Strict SNI Checking

By default, if the client does not send SNI, or if no certificate matches the requested server name,
Traefik falls back to the [default certificate](#default-certificate) from the TLS store (if configured).

To reject connections without SNI (or with an unknown server name) instead of falling back to the default certificate,
enable `sniStrict` in [TLS Options](./tls-options.md#strict-sni-checking).

## Certificates Stores

In Traefik, certificates are grouped together in certificates stores.

> **Important — Restriction**
>
> Any store definition other than the default one (named `default`) will be ignored,
> and there is therefore only one globally available TLS store.

In the `tls.certificates` section, a list of stores can then be specified to indicate where the certificates should be stored:

**Structured (YAML)**

```yaml
tls:
  certificates:
    - certFile: /path/to/domain.cert
      keyFile: /path/to/domain.key
      stores:
        - default
    # Note that since no store is defined,
    # the certificate below will be stored in the `default` store.
    - certFile: /path/to/other-domain.cert
      keyFile: /path/to/other-domain.key
```

**Structured (TOML)**

```toml
[[tls.certificates]]
  certFile = "/path/to/domain.cert"
  keyFile = "/path/to/domain.key"
  stores = ["default"]

[[tls.certificates]]
  # Note that since no store is defined,
  # the certificate below will be stored in the `default` store.
  certFile = "/path/to/other-domain.cert"
  keyFile = "/path/to/other-domain.key"
```

> **Important — Restriction**
>
> The `stores` list will actually be ignored and automatically set to `["default"]`.

> **Tip — Per provider examples**
>
> - [Docker: Enable TLS](../../../../expose/docker/basic.md#enable-tls)
> - [Swarm: Enable TLS](../../../../expose/swarm/basic.md#enable-tls)
> - [Kubernetes: Enable TLS](../../../../expose/kubernetes/basic.md#enable-tls)

### Default Certificate

Traefik can use a default certificate for connections without a SNI, or without a matching domain.
This default certificate should be defined in a TLS store:

**Structured (YAML)**

```yaml
tls:
  stores:
    default:
      defaultCertificate:
        certFile: path/to/cert.crt
        keyFile: path/to/cert.key
```

**Structured (TOML)**

```toml
[tls.stores]
  [tls.stores.default]
    [tls.stores.default.defaultCertificate]
      certFile = "path/to/cert.crt"
      keyFile  = "path/to/cert.key"
```

If no `defaultCertificate` is provided, Traefik will use the generated one.

### ACME Default Certificate

You can configure Traefik to use an ACME provider (like Let's Encrypt) to generate the default certificate.
The configuration to resolve the default certificate should be defined in a TLS store:

> **Important — Precedence with the `defaultGeneratedCert` option**
>
> The `defaultGeneratedCert` definition takes precedence over the ACME default certificate configuration.

**Structured (YAML)**

```yaml
tls:
  stores:
    default:
      defaultGeneratedCert:
        resolver: myresolver
        domain:
          main: example.org
          sans:
            - foo.example.org
            - bar.example.org
```

**Structured (TOML)**

```toml
[tls.stores]
  [tls.stores.default.defaultGeneratedCert]
    resolver = "myresolver"
    [tls.stores.default.defaultGeneratedCert.domain]
      main = "example.org"
      sans = ["foo.example.org", "bar.example.org"]
```

**Labels**

```yaml
labels:
  - "traefik.tls.stores.default.defaultgeneratedcert.resolver=myresolver"
  - "traefik.tls.stores.default.defaultgeneratedcert.domain.main=example.org"
  - "traefik.tls.stores.default.defaultgeneratedcert.domain.sans=foo.example.org, bar.example.org"
```

**Tags**

```json
{
  "Name": "default",
  "Tags": [
    "traefik.tls.stores.default.defaultgeneratedcert.resolver=myresolver",
    "traefik.tls.stores.default.defaultgeneratedcert.domain.main=example.org",
    "traefik.tls.stores.default.defaultgeneratedcert.domain.sans=foo.example.org, bar.example.org"
  ]
}
```

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
