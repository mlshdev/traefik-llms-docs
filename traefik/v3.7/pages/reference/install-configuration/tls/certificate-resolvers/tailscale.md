---
title: "Traefik Tailscale Documentation"
description: "Learn how to configure Traefik Proxy to resolve TLS certificates for your Tailscale services. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Install Configuration / TLS / Certificate Resolvers / Tailscale"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/install-configuration/tls/certificate-resolvers/tailscale.md"
source_url: "https://github.com/traefik/traefik/blob/21a4ca1fad46ceca9b7d7903eeaf3721325f3e50/docs/content/reference/install-configuration/tls/certificate-resolvers/tailscale.md"
---

# Tailscale

Provision TLS certificates for your internal Tailscale services.

To protect a service with TLS, a certificate from a public Certificate Authority is needed.
In addition to its vpn role, Tailscale can also [provide certificates](https://tailscale.com/kb/1153/enabling-https/) for the machines in your Tailscale network.

## Configuration Example

To obtain a TLS certificate from the Tailscale daemon,
a Tailscale certificate resolver needs to be configured as below.

> **Example — Enabling Tailscale certificate resolution**
>
> **File (YAML)**
>
> ```yaml
> entryPoints:
>   web:
>     address: ":80"
>
>   websecure:
>     address: ":443"
>
> certificatesResolvers:
>   myresolver:
>     tailscale: {}
> ```
>
> **File (TOML)**
>
> ```toml
> [entryPoints]
>   [entryPoints.web]
>     address = ":80"
>
>   [entryPoints.websecure]
>     address = ":443"
>
> [certificatesResolvers.myresolver.tailscale]
> ```
>
> **CLI**
>
> ```bash
> --entrypoints.web.address=:80
> --entrypoints.websecure.address=:443
> # ...
> --certificatesresolvers.myresolver.tailscale=true
> ```

> **Example — Domain from Router's Rule Example**
>
> **Docker & Swarm**
>
> ```yaml
> labels:
>   - traefik.http.routers.blog.rule=Host(`monitoring.yak-bebop.ts.net`) && Path(`/metrics`)
>   - traefik.http.routers.blog.tls.certresolver=myresolver
> ```
>
> **Docker (Swarm)**
>
> ```yaml
> deploy:
>   labels:
>     - traefik.http.routers.blog.rule=Host(`monitoring.yak-bebop.ts.net`) && Path(`/metrics`)
>     - traefik.http.routers.blog.tls.certresolver=myresolver
> ```
>
> **Kubernetes**
>
> ```yaml
> apiVersion: traefik.io/v1alpha1
> kind: IngressRoute
> metadata:
>   name: blogtls
> spec:
>   entryPoints:
>     - websecure
>   routes:
>     - match: Host(`monitoring.yak-bebop.ts.net`) && Path(`/metrics`)
>       kind: Rule
>       services:
>         - name: blog
>           port: 8080
>   tls:
>     certResolver: myresolver
> ```
>
> **File (YAML)**
>
> ```yaml
> ## Dynamic configuration
> http:
>   routers:
>     blog:
>       rule: "Host(`monitoring.yak-bebop.ts.net`) && Path(`/metrics`)"
>       tls:
>         certResolver: myresolver
> ```
>
> **File (TOML)**
>
> ```toml
> ## Dynamic configuration
> [http.routers]
>   [http.routers.blog]
>   rule = "Host(`monitoring.yak-bebop.ts.net`) && Path(`/metrics`)"
>   [http.routers.blog.tls]
>     certResolver = "myresolver"
> ```

> **Example — Domain from Router's tls.domain Example**
>
> **Docker & Swarm**
>
> ```yaml
> labels:
>   - traefik.http.routers.blog.rule=Path(`/metrics`)
>   - traefik.http.routers.blog.tls.certresolver=myresolver
>   - traefik.http.routers.blog.tls.domains[0].main=monitoring.yak-bebop.ts.net
> ```
>
> **Docker (Swarm)**
>
> ```yaml
> deploy:
>   labels:
>     - traefik.http.routers.blog.rule=Path(`/metrics`)
>     - traefik.http.routers.blog.tls.certresolver=myresolver
>     - traefik.http.routers.blog.tls.domains[0].main=monitoring.yak-bebop.ts.net
> ```
>
> **Kubernetes**
>
> ```yaml
> apiVersion: traefik.io/v1alpha1
> kind: IngressRoute
> metadata:
>   name: blogtls
> spec:
>   entryPoints:
>     - websecure
>   routes:
>     - match: Path(`/metrics`)
>       kind: Rule
>       services:
>         - name: blog
>           port: 8080
>   tls:
>     certResolver: myresolver
>     domains:
>       - main: monitoring.yak-bebop.ts.net
> ```
>
> **File (YAML)**
>
> ```yaml
> http:
>   routers:
>     blog:
>       rule: "Path(`/metrics`)"
>       tls:
>         certResolver: myresolver
>         domains:
>           - main: "monitoring.yak-bebop.ts.net"
> ```
>
> **File (TOML)**
>
> ```toml
> ## Dynamic configuration
> [http.routers]
>   [http.routers.blog]
>     rule = "Path(`/metrics`)"
>     [http.routers.blog.tls]
>       certResolver = "myresolver"
>       [[http.routers.blog.tls.domains]]
>         main = "monitoring.yak-bebop.ts.net"
> ```

> **Info — Referencing a certificate resolver**
>
> Defining a certificate resolver does not imply that routers are going to use it automatically.
> Each router or entrypoint that is meant to use the resolver must explicitly [reference](../../../routing-configuration/http/routing/router.md#opt-tls-certResolver) it.

## Domain Definition

A certificate resolver requests certificates for a set of domain names inferred from routers, according to the following:

- If the router has a `tls.domains` option set, then the certificate resolver derives this router domain name from the main option of `tls.domains`.

- Otherwise, the certificate resolver derives the domain name from any `Host()` or `HostSNI()` matchers in the router's rule.

> **Info — Tailscale Domain Format**
>
> A domain is only considered if it is a Tailscale-specific one—that is, in the form `machine-name.domains-alias.ts.net`.

## Tailscale Certificates Renewal

Traefik automatically tracks the expiry date of each Tailscale certificate it fetches and starts to renew a certificate 14 days before its expiry to match the Tailscale daemon renewal policy.
