---
title: "Content-Length"
description: "Enforce strict Content‑Length validation in Traefik by streaming or full buffering to prevent truncated or over‑long requests and responses. Read the technical documentation."
section: "Reference"
breadcrumb: "Reference / Security / Content-Length"
traefik_version: "v3.7"
upstream_path: "docs/content/security/content-length.md"
source_url: "https://github.com/traefik/traefik/blob/21a4ca1fad46ceca9b7d7903eeaf3721325f3e50/docs/content/security/content-length.md"
---

Traefik acts as a streaming proxy. By default, it checks each chunk of data against the `Content-Length` header as it passes it on to the backend or client.
This live check blocks truncated or over‑long streams without holding the entire message.

If you need Traefik to read and verify the full body before any data moves on, add the [buffering middleware](../reference/routing-configuration/http/middlewares/buffering.md):

```yaml
http:
  middlewares:
    buffer-and-validate:
      buffering: {}
```

With buffering enabled, Traefik will:

- Read the entire request or response into memory.
- Compare the actual byte count to the `Content-Length` header.
- Reject the message if the counts do not match.

> **Warning**
>
> Buffering adds overhead. Every request and response is held in full before forwarding, which can increase memory use and latency.
> Use it when strict content validation is critical to your security posture.
