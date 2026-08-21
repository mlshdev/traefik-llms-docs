---
title: "Traefik V3 Migration Documentation"
description: "Migrate from Traefik Proxy v2 to v3 and update all the necessary configurations to take advantage of all the improvements. Read the technical documentation."
section: "Migrate"
breadcrumb: "Migrate / Traefik v2 to v3 / Migration guide"
traefik_version: "v3.7"
upstream_path: "docs/content/migrate/v2-to-v3.md"
source_url: "https://github.com/traefik/traefik/blob/b78307590625ada3e430d358b7947f11a0aef226/docs/content/migrate/v2-to-v3.md"
---

# Migration Guide: From v2 to v3

How to Migrate from Traefik v2 to Traefik v3.

> **Success — Streamlined Migration Process**
>
> Traefik v3 introduces minimal breaking changes and maintains backward compatibility with v2 syntax in routing configuration, offering a gradual migration path.

With Traefik v3, we are introducing a streamlined transition process from v2. Minimal breaking changes have been made to specific options in the [install configuration](./v2-to-v3-details.md#install-configuration-changes "Link to install configuration changes"), and we are ensuring backward compatibility with v2 syntax in the [routing configuration](./v2-to-v3-details.md#routing-configuration-changes "Link to routing configuration changes"). This will offer a gradual path for adopting the v3 syntax, allowing users to progressively migrate their Kubernetes ingress resources, Docker labels, etc., to the new format.

## Migration Overview

The migration process consists of three progressive steps designed to minimize risk and ensure a smooth transition:

> **Abstract — Migration Steps**
>
> **Step 1:** [Prepare configurations and test v3](#step-1-prepare-configurations-and-test-v3)
> **Step 2:** [Migrate production instances to Traefik v3](#step-2-migrate-production-instances-to-traefik-v3)
> **Step 3:** [Progressively migrate routing configuration](#step-3-progressively-migrate-routing-configuration)

---

## Step 1: Prepare Configurations and Test v3

> **Info — Preparation Phase**
>
> This step focuses on updating install configurations and enabling backward compatibility for a safe testing environment.

### Configuration Updates

**Review and Update install Configuration**

Check the changes in [install configurations](./v2-to-v3-details.md#install-configuration-changes "Link to install configuration changes") and [operations](./v2-to-v3-details.md#operations-changes "Link to operations changes") brought by Traefik v3. Modify your configurations accordingly.

**Enable v2 Compatibility Mode**

Add the following configuration to maintain v2 syntax compatibility:

```yaml
# install configuration
core:
  defaultRuleSyntax: v2
```

> **Note — Backward Compatibility**
>
> This snippet in the install configuration makes the [v2 format](./v2-to-v3-details.md#configure-the-default-syntax-in-install-configuration "Link to configure default syntax in install config") the default rule matchers syntax.

### Testing Phase

**Start Your Test Environment**

1. Start Traefik v3 with the updated configuration
2. Monitor the startup logs for any errors
3. Test routing to your applications

**Validation Checklist**

- ✅ Traefik starts without error logs
- ✅ All routes are functioning correctly  
- ✅ Applications are accessible through Traefik

> **Success — Ready for Next Step**
>
> If you don't get any error logs while testing, you are good to go! Otherwise, follow the remaining migration options highlighted in the logs.

Once your Traefik test instances are starting and routing to your applications, proceed to the next step.

---

## Step 2: Migrate Production Instances to Traefik v3

> **Warning — Production Migration**
>
> This is the critical step where you migrate your production environment. Proper monitoring and rollback preparation are essential.

### Migration Strategy

**Progressive Deployment**

We strongly advise you to follow a progressive migration strategy ([Kubernetes rolling update mechanism](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/ "Link to the Kubernetes rolling update documentation"), for example) to migrate your production instances to v3.

**Required Preparations**

> **Danger — Critical Requirements**
>
> - ✅ **Real-time monitoring solution** for ingress traffic ([monitoring guide](https://traefik.io/blog/capture-traefik-metrics-for-apps-on-kubernetes-with-prometheus/ "Link to the blog on capturing Traefik metrics with Prometheus"))
> - ✅ **Rollback plan** ready for immediate execution
> - ✅ **Team availability** during migration window

### Migration Execution

**During Migration:**

1. **Monitor continuously:** Watch ingress traffic for any errors or anomalies
2. **Be prepared to rollback:** Have your rollback procedure ready to execute immediately
3. **Use debug logs:** Leverage debug and access logs to understand any issues that arise

**Validation Steps:**

- Monitor response times and error rates
- Verify all critical application paths are working
- Check that SSL/TLS termination is functioning correctly
- Validate middleware behavior

> **Success — Migration Complete**
>
> Once every Traefik instance is updated, you will be on Traefik v3!

---

## Step 3: Progressively Migrate Routing Configuration

> **Info — Optional Immediate Step**
>
> This step can be done later in the process, as Traefik v3 is compatible with the v2 format for [routing configuration](./v2-to-v3-details.md#routing-configuration-changes "Link to routing configuration changes"). Enable Traefik logs to get some help if any deprecated option is in use.

### Migration Process

**Review Routing Configuration Changes**

Check the changes in [routing configuration](./v2-to-v3-details.md#routing-configuration-changes "Link to routing configuration changes") to understand what updates are needed.

**Progressive Router Migration**

1. **Select a router** to migrate first (start with non-critical services)
2. **[Switch to v3 syntax](./v2-to-v3-details.md#configure-the-syntax-per-router "Link to configuring the syntax per router")** for that specific router
3. **Test thoroughly** to ensure ingress traffic is not impacted
4. **Deploy and validate** the updated resource
5. **Remove the old v2 resource** once validation is complete
6. **Repeat** for each remaining router

### Migration Best Practices

> **Tip — Migration Strategy**
>
> - Start with development or staging environments
> - Migrate one service at a time
> - Test each migration thoroughly before proceeding
> - Keep detailed logs of what was changed

### Final Configuration Cleanup

Once all Ingress resources are migrated to v3 syntax, remove the compatibility configuration:

```yaml
# Remove this from install configuration
core:
  defaultRuleSyntax: v2  # ← Delete this entire section
```

> **Success — 🎉 Migration Complete!**
>
> You are now fully migrated to Traefik v3 and can take advantage of all the new features and improvements!

### Post-Migration Verification

**Final Checklist:**

- ✅ All routers use v3 syntax
- ✅ v2 compatibility mode disabled
- ✅ No deprecated warnings in logs
- ✅ All applications functioning correctly
- ✅ Performance metrics stable

---

> **Question — Using Traefik OSS in Production?**
>
> If you are using Traefik at work, consider adding enterprise-grade API gateway capabilities or commercial support for Traefik OSS.
>
> - [Watch our API Gateway Demo Video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc)
> - [Request 24/7/365 OSS Support](https://info.traefik.io/request-commercial-support?cta=doc)
>
> Adding API Gateway capabilities to Traefik OSS is fast and seamless. There's no rip and replace and all configurations remain intact. See it in action via [this short video](https://info.traefik.io/watch-traefik-api-gw-demo?cta=doc).
