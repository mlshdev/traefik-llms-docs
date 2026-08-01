---
title: "Certificates Resolver"
description: "Automatic Certificate Management using Let's Encrypt/Vault and Tailscale."
section: "Reference"
breadcrumb: "Reference / Install Configuration / TLS / Certificate Resolvers / Overview"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/tls/certificate-resolvers/overview.md"
source_url: "https://github.com/traefik/traefik/blob/2a2349356c01b1b1f7ecddb0c17b30c97f5241e7/docs/content/reference/install-configuration/tls/certificate-resolvers/overview.md"
---

In Traefik, TLS Certificates can be generated using Certificates Resolvers.

In Traefik, two certificate resolvers exist:

- [`acme`](./acme.md): It allows generating ACME certificates stored in a file (not distributed).
- [`tailscale`](./tailscale.md): It allows provisioning TLS certificates for internal Tailscale services.

The Certificates resolvers are defined in the static configuration.

> **Note — Referencing a certificate resolver**
>
> Defining a certificate resolver does not imply that routers are going to use it automatically.
> Each router or entrypoint that is meant to use the resolver must explicitly reference it.

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
