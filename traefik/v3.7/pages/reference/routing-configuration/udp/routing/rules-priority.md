---
title: "Traefik UDP Routers Rules & Priority Documentation"
description: "In Traefik Proxy, a router is in charge of connecting incoming requests to the Services that can handle them. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Routing Configuration / Common Configuration / UDP / Routing / Rules & Priority"
traefik_version: "v3.7"
upstream_path: "docs/content/reference/routing-configuration/udp/routing/rules-priority.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/reference/routing-configuration/udp/routing/rules-priority.md"
---

A router is in charge of connecting incoming requests to the services that can handle them.

Similarly to TCP, as UDP is the transport layer, there is no concept of a request,
so there is no notion of an URL path prefix to match an incoming UDP packet with.
Furthermore, as there is no good TLS support at the moment for multiple hosts,
there is no Host SNI notion to match against either.
Therefore, there is no criterion that could be used as a rule to match incoming packets in order to route them.
So UDP _routers_ at this time are pretty much only load-balancers in one form or another.

> **Tip**
>
> UDP routers can only target UDP services (and not HTTP or TCP services).

## Sessions and timeout

Even though UDP is connectionless (and because of that),
the implementation of an UDP router in Traefik relies on what we (and a couple of other implementations) call a `session`.
It means that some state is kept about an ongoing communication between a client and a backend,
notably so that the proxy knows where to forward a response packet from a backend.

As expected, a `timeout` is associated to each of these sessions,
so that they get cleaned out if they go through a period of inactivity longer than a given duration.

Timeout can be configured using the `entryPoints.name.udp.timeout` option as described under [EntryPoints](../../../install-configuration/entrypoints.md)

## EntryPoints

If not specified, UDP routers will accept packets from all defined (UDP) EntryPoints. If one wants to limit the router scope to a set of EntryPoints, one should set the `entryPoints` option.

## Configuration Example

Listens to Every Entry Point

**Structured (YAML)**

```yaml
udp:
  routers:
    Router-1:
      # By default, routers listen to all UDP entrypoints
      # i.e. "other", and "streaming".
      service: "service-1"
```

**Structured (TOML)**

```toml
[udp.routers]
  [udp.routers.Router-1]
    # By default, routers listen to all UDP entrypoints,
    # i.e. "other", and "streaming".
    service = "service-1"
```

**Labels**

```yaml
labels:
  - "traefik.udp.routers.Router-1.service=service-1"
```

**Tags**

```json
{
  //...
  "Tags": [
    "traefik.udp.routers.Router-1.service=service-1"
  ]
}
```

Listens to Specific EntryPoints

**Structured (YAML)**

```yaml
udp:
  routers:
    Router-1:
      # does not listen on "other" entry point
      entryPoints:
        - "streaming"
      service: "service-1"
```

**Structured (TOML)**

```toml
[udp.routers]
  [udp.routers.Router-1]
    # does not listen on "other" entry point
    entryPoints = ["streaming"]
    service = "service-1"
```

**Labels**

```yaml
labels:
  - "traefik.udp.routers.Router-1.entryPoints=streaming"
  - "traefik.udp.routers.Router-1.service=service-1"
```

**Tags**

```json
{
  //...
  "Tags": [
    "traefik.udp.routers.Router-1.entryPoints=streaming",
    "traefik.udp.routers.Router-1.service=service-1"
  ]
}
```

> **Info — Service**
>
> There must be one (and only one) UDP [service](../service.md) referenced per UDP router.
> Services are the target for the router.

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
