---
title: "Feature Deprecation Notices"
section: "Reference"
breadcrumb: "Reference / Deprecation Notices / Features"
traefik_version: "v3.7"
upstream_path: "docs/content/deprecation/features.md"
source_url: "https://github.com/traefik/traefik/blob/8bd3bd277758ca6e70ce38b132039186a01812a9/docs/content/deprecation/features.md"
---

# Feature Deprecation Notices

This page is maintained and updated periodically to reflect our roadmap and any decisions around feature deprecation.

| Feature                                                                                                              | Deprecated | End of Support | Removal |
|----------------------------------------------------------------------------------------------------------------------|------------|----------------|---------|
| [Kubernetes Ingress API Version `networking.k8s.io/v1beta1`](#kubernetes-ingress-api-version-networkingk8siov1beta1) | N/A        | N/A            | 3.0     |
| [CRD API Version `apiextensions.k8s.io/v1beta1`](#kubernetes-ingress-api-version-networkingk8siov1beta1)             | N/A        | N/A            | 3.0     |

## Impact

### Kubernetes Ingress API Version `networking.k8s.io/v1beta1`

The Kubernetes Ingress API Version `networking.k8s.io/v1beta1` support is removed in v3. 
Please use the API Group `networking.k8s.io/v1` instead.

### Traefik CRD Definitions API Version `apiextensions.k8s.io/v1beta1`

The Traefik CRD definitions API Version `apiextensions.k8s.io/v1beta1` support is removed in v3.
Please use the API Group `apiextensions.k8s.io/v1` instead.
