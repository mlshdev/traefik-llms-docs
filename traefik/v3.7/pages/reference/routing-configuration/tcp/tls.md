---
title: "Traefik TLS Documentation"
description: "Learn how to configure the transport layer security (TLS) connection for TCP services in Traefik Proxy. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / TCP / TLS"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/tcp/tls.md"
source_url: "https://github.com/traefik/traefik/blob/e80aaab074b4cc5acee6e2bf516b52d8bf3cb3bf/docs/content/reference/routing-configuration/tcp/tls.md"
---

## General

When a TCP router is configured to handle TLS traffic, include a `tls` field in its definition. This field tells Traefik that the router should process only TLS connections and ignore non-TLS traffic.

By default, a router with a TLS field will terminate the TLS connections, meaning that it will send decrypted data to the services.

## Configuration Example

**Structured (YAML)**

```yaml
tcp:
  routers:
    my-tls-router:
      rule: "HostSNI(`example.com`)"
      service: "my-tcp-service"
      tls:
        passthrough: true
        options: "my-tls-options"
        domains:
          - main: "example.com"
            sans:
              - "www.example.com"
              - "api.example.com"
        certResolver: "myresolver"
```

**Structured (TOML)**

```toml
[tcp.routers.my-tls-router]
  rule = "HostSNI(`example.com`)"
  service = "my-tcp-service"

  [tcp.routers.my-tls-router.tls]
    passthrough = true
    options = "my-tls-options"
    certResolver = "myresolver"

    [[tcp.routers.my-tls-router.tls.domains]]
      main = "example.com"
      sans = ["www.example.com", "api.example.com"]
```

**Labels**

```yaml
labels:
  - "traefik.tcp.routers.my-tls-router.tls=true"
  - "traefik.tcp.routers.my-tls-router.rule=HostSNI(`example.com`)"
  - "traefik.tcp.routers.my-tls-router.service=my-tcp-service"
  - "traefik.tcp.routers.my-tls-router.tls.passthrough=true"
  - "traefik.tcp.routers.my-tls-router.tls.options=my-tls-options"
  - "traefik.tcp.routers.my-tls-router.tls.certResolver=myresolver"
  - "traefik.tcp.routers.my-tls-router.tls.domains[0].main=example.com"
  - "traefik.tcp.routers.my-tls-router.tls.domains[0].sans=www.example.com,api.example.com"
```

**Tags**

```json
{
  //...
  "Tags": [
    "traefik.tcp.routers.my-tls-router.tls=true",
    "traefik.tcp.routers.my-tls-router.rule=HostSNI(`example.com`)",
    "traefik.tcp.routers.my-tls-router.service=my-tcp-service",
    "traefik.tcp.routers.my-tls-router.tls.passthrough=true",
    "traefik.tcp.routers.my-tls-router.tls.options=my-tls-options",
    "traefik.tcp.routers.my-tls-router.tls.certResolver=myresolver",
    "traefik.tcp.routers.my-tls-router.tls.domains[0].main=example.com",
    "traefik.tcp.routers.my-tls-router.tls.domains[0].sans=www.example.com,api.example.com"
  ]
}
```

> **Info — Postgres STARTTLS**
>
> Traefik supports the Postgres STARTTLS protocol,
> which allows TLS routing for Postgres connections.
>
> To do so, Traefik reads the first bytes sent by a Postgres client,
> identifies if they correspond to the message of a STARTTLS negotiation,
> and, if so, acknowledges and signals the client that it can start the TLS handshake.
>
> Please note/remember that there are subtleties inherent to STARTTLS in whether the connection ends up being a TLS one or not.
> These subtleties depend on the `sslmode` value in the client configuration (and on the server authentication rules).
> Therefore, it is recommended to use the `require` value for the `sslmode`.
>
> Afterwards, the TLS handshake, and routing based on TLS, can proceed as expected.
>
> > **Warning — Postgres STARTTLS with TCP TLS PassThrough routers**
> >
> > As mentioned above, the `sslmode` configuration parameter does have an impact on whether a STARTTLS session will succeed.
> > In particular in the context of TCP TLS PassThrough, some of the values (such as `allow`) do not even make sense.
> > Which is why, once more it is recommended to use the `require` value.

## Configuration Options

| Field                                                                              | Description                                                                                                                                                                                                    | Default | Required |
|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------|
| <a id="opt-passthrough" href="#opt-passthrough" title="#opt-passthrough">`passthrough`</a> | Defines whether the requests should be forwarded "as is", keeping all data encrypted.                                                                                                                          | false   | No       |
| <a id="opt-options" href="#opt-options" title="#opt-options">`options`</a> | enables fine-grained control of the TLS parameters. It refers to a [TLS Options](../http/tls/tls-options.md) and will be applied only if a `HostSNI` rule is defined.                                          | ""      | No       |
| <a id="opt-certResolver" href="#opt-certResolver" title="#opt-certResolver">`certResolver`</a> | The name of the certificate resolver to use for automatic certificate generation via ACME providers (such as Let's Encrypt). See the [Certificate Resolver](tls.md#certificate-resolver) section for more details. | ""      | No       |
| <a id="opt-domains" href="#opt-domains" title="#opt-domains">`domains`</a> | List of domains and Subject Alternative Names (SANs) for explicit certificate domain specification. See the [Custom Domains](tls.md#custom-domains) section for more details.                                      | []      | No       |

## Certificate Resolver

The `tls.certResolver` option allows you to specify a certificate resolver for automatic certificate generation via ACME providers (such as Let's Encrypt).

When a certificate resolver is configured for a router,
Traefik will automatically obtain and manage TLS certificates for the domains specified in the router's rule (in the `HostSNI` matcher) or in the `tls.domains` configuration (with `tls.domains` taking precedence).

> **Important — Prerequisites**
>
> - Certificate resolvers must be defined in the [static configuration](../../install-configuration/tls/certificate-resolvers/acme.md)
> - The router must have `tls` enabled
> - An ACME challenge type must be configured for the certificate resolver

## Custom Domains

When using ACME certificate resolvers, domains are automatically extracted from router rules,
but the `tls.domains` option allows you to explicitly specify the domains and Subject Alternative Names (SANs) for which certificates should be generated.

This provides fine-grained control over certificate generation and takes precedence over domains automatically extracted from router rules.

Every domain must have A/AAAA records pointing to Traefik.

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
