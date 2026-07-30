---
title: "Traefik V2 Migration Documentation"
description: "Migrate from Traefik Proxy v1 to v2 and update all the necessary configurations to take advantage of all the improvements. Read the technical documentation."
section: "Migrate"
breadcrumb: "Migrate / Traefik v1 to v2"
traefik_version: "v3.7"
upstream_path: "docs/content/migrate/v1-to-v2.md"
source_url: "https://github.com/traefik/traefik/blob/e80aaab074b4cc5acee6e2bf516b52d8bf3cb3bf/docs/content/migrate/v1-to-v2.md"
---

# Migration Guide: From v1 to v2

How to Migrate from Traefik v1 to Traefik v2.

The version 2 of Traefik introduced a number of breaking changes,
which require one to update their configuration when they migrate from v1 to v2.

For more information about the changes in Traefik v2, please refer to the [v2 documentation](https://doc.traefik.io/traefik/v2.11/migration/v1-to-v2/).

> **Info — Migration Helper**
>
> We created a tool to help during the migration: [traefik-migration-tool](https://github.com/traefik/traefik-migration-tool)
>
> This tool lets you:
>
> - convert `Ingress` to Traefik `IngressRoute` resources.
> - convert `acme.json` file from v1 to v2 format.
> - migrate the static configuration contained in the file `traefik.toml` to a Traefik v2 file.
