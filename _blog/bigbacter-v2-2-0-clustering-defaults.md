---
title: "BigBacter v2.2.0: New Clustering Defaults"
layout: page
date: 2026-11-09
author: Jared Johnson
description: BigBacter v2.2.0 updates Floc to v1.2.4, adds a new assign hash frequency setting, raises the default cluster distance to 0.1, and records database settings in config.json.
nav_order: -20261109
---

# {{ page.title }}
{: .no_toc }

<small>{{ page.date | date: "%B %-d, %Y" }} · {{ page.author }}</small>

1. TOC
{:toc}

---

# TL;DR

|What|Before (v2.0–v2.1)|Now (v2.2.0)|
|:-|:-|:-|
|Floc|v1.1|v1.2.4|
|`--clust_dist`|`0.03`|`0.1`|
|`--clust_assign_hashfreq`|Not available (behaved like `0`)|`0.6`|
|Database settings|Not recorded|Saved to `<db>/<taxa>/config.json` and checked on every run|

{: .important }
> **We strongly recommend rebuilding existing databases with the new defaults.** Runs against a database created before v2.2.0 will fail until it is rebuilt or given a `config.json`. See [Upgrading](#upgrading-your-database).

---

# The problem: clusters changed depending on how samples were added
BigBacter is built for routine surveillance. Samples arrive incrementally, often in uneven batches, so each sample must land in the same cluster no matter when or how it is added. In BigBacter v2.1.1, some samples clustered differently depending on how they were added to the database. We traced this to how [Floc](https://github.com/NW-PaGe/floc) assigns new samples to existing clusters.

The diagram below depicts how **BigBacter v2.1.1** used floc v1.1 to create and assign clusters:
![Floc assignment using the union of cluster hashes]({{ site.baseurl }}/assets/media/blog/floc_cluster_flow_union.svg)

{: .note}
Notice that the new sample is not assigned to the existing cluster because all cluster hashes are included in the comparison.

---

# The fix: `--clust_assign_hashfreq`

Floc v1.2.3 added `--assign-hash-freq`, which BigBacter v2.2.0 exposes as `--clust_assign_hashfreq` (default `0.6`). It sets which hashes go into each cluster's merged sketch: only hashes found in at least that fraction of the cluster's members.

- **`0.6` (new default):** the merged sketch keeps the hashes shared by most members, a consensus that stays close to the size of a single genome. The distance from a new sample to a cluster no longer depends on how big or diverse the cluster has become.
- **`0` (old behavior):** the merged sketch keeps every hash from every member. Do not use this for new databases.

This setting only affects how new samples are assigned to existing clusters. Samples clustered together in the same run are compared with each other directly.

The diagram shows how **BigBacter v2.2.0** uses floc v1.2.4 to assign clusters after filtering cluster hashes:
![Floc assignment using filtered cluster hashes]({{ site.baseurl }}/assets/media/blog/floc_cluster_flow_filtered.svg)

{: .note}
Notice that the new sample is now assigned to the cluster becuase only the most common hashes are included in the comparison.

---

# How the new defaults were chosen

The new defaults come from a [Floc evaluation of distance vs. assign hash frequency](https://github.com/NW-PaGe/floc/blob/main/docs/evals/dist_vs_assign-hash-freq/README.md). In brief:

- **Datasets:** 100 assemblies each of _Escherichia coli_, _Acinetobacter baumannii_, and _Staphylococcus aureus_.
- **Design:** the same samples were added in batches of 1, 10, and 50, in the same order, and the final clusters were compared with a reference run that clustered all 100 samples at once. Batch size 1 mirrors a database that is updated one sample at a time.
- **Settings tested:** distances of `0.05`, `0.075`, and `0.1`, each with an assign hash frequency of `0` and `0.6`.
- **Benchmark:** pairs of samples placed in different clusters were checked against their SNP distance. Separating samples within 10 SNPs ruled a combination out, and separating samples within 100 SNPs was a major penalty.

|Distance|Assign hash freq|Closest pair split (SNPs)|Close pairs split (worst run)|Samples reassigned (worst run)|Verdict|
|-|-|-|-|-|-|
|0.05|0|**0**|**570**|58|Ruled out|
|0.05|0.6|**0**|**75**|30|Ruled out|
|0.075|0|**0**|**579**|50|Ruled out|
|0.075|0.6|none|0|5|Option for smaller clusters|
|0.1|0|**0**|**569**|42|Ruled out|
|0.1|0.6|none|0|2|**New default**|

_"Close pairs" are samples within 100 SNPs of each other. Results combine all three organisms. See the [full evaluation](https://github.com/NW-PaGe/floc/blob/main/docs/evals/dist_vs_assign-hash-freq/README.md) for per-organism tables, metric definitions, and interactive trees._

Key findings:

1. **Assignment against the union sketch produced inconsistent clusters.** With an assign hash frequency of 0, every distance threshold tested separated identical _A. baumannii_ samples (0 SNPs apart). Up to 579 of 1,140 pairs within 100 SNPs (50.8%) were separated in a single run.
2. **An assign hash frequency of 0.6 resolved the inconsistency at distances of 0.075 and above.** No pair of samples within 100 SNPs was separated in any run. At a distance of 0.1, all _A. baumannii_ and _S. aureus_ runs matched their reference clusters exactly, and no run reassigned more than 2 samples relative to its reference.
3. **Lower distance thresholds remained unstable.** At a distance of 0.05, an assign hash frequency of 0.6 still separated up to 75 _A. baumannii_ pairs within 100 SNPs, including identical samples. The previous BigBacter default of 0.03 was not tested, but it is below this threshold.

## Trade-off: consistency vs. cluster diversity

Higher distance thresholds produce larger and more genetically diverse clusters, which can reduce the size of the shared core genome. In the _E. coli_ reference runs, the maximum pairwise SNP distance within a single cluster was 4,134 at a distance of 0.1, compared with 2,168 at 0.075. A distance of 0.075 with an assign hash frequency of 0.6 also separated no pairs within 100 SNPs, and no run reassigned more than 5 samples relative to its reference. It is therefore a reasonable alternative where smaller clusters are preferred.

Each database should use a single distance threshold throughout its lifetime. Starting with v2.2.0, BigBacter enforces this (see below).

---

# New: `config.json` records how each database was built

Each taxa database now has a `<db>/<taxa>/config.json` that records the settings it was created with:

```json
{
  "clust_dist": 0.1,
  "clust_assign_hashfreq": 0.6,
  "floc_version": "1.2.4",
  "bigbacter_version": "2.2.0"
}
```

This new config file is used in the following manner:

|Condition|Result|
|:-|:-|
|`config.json` is missing|Run fails|
|`--clust_dist` differs from the recorded value|Run fails|
|`--clust_assign_hashfreq` differs from the recorded value|Warning only|

This prevents a database from quietly being extended with a different distance than the one it was built with. See [Database Config]({{ site.baseurl }}/docs/v2.0/pages/outputs/database#database-config-configjson) for details.

---

---

# Upgrading your database

## Recommended: rebuild

1. Point `--db` at a **new, empty** location.
2. Run all previously processed samples through BigBacter v2.2.0 with `--push true`, using the default `--clust_dist` and `--clust_assign_hashfreq`.

---

# Links

- [Floc evaluation: distance vs. assign hash frequency](https://github.com/NW-PaGe/floc/blob/main/docs/evals/dist_vs_assign-hash-freq/README.md)
- [BigBacter changelog](https://github.com/NW-PaGe/bigbacter/blob/main/CHANGELOG.md)
- [Clustering parameters]({{ site.baseurl }}/docs/v2.0/pages/inputs/#clustering-options)
