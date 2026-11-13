---
title: bb-utils
layout: page
nav_order: 1
parent: Auxillary Workflows
permalink: /docs/auxillary/pages/bb-utils/
---

# {{ page.title }}
{: .no_toc}

1. TOC
{:toc}

## Overview

[bb-utils](https://github.com/nw-page/bb-utils) is a companion workflow for managing [BigBacter databases]({{ site.baseurl }}/docs/v2.0/pages/outputs/database). 

It has three modes:

|Mode|Function|
|:-|:-|
|`summary`|Create a summary of the database (read-only).|
|`remove`|Remove samples by name, cluster, or date added.|
|`push`|Push files from a BigBacter run to the database.|

bb-utils is written in Nextflow, which means it works with local and cloud-based storage systems (or a mixture of the both!). The workflow is _process-free_, which means the only dependencies are Nextflow (v25.04 or later) and any software required by your cloud provider (if you use one; e.g., AWS CLI). 

{: .important}
`bb-utils` is compatible with BigBacter v2.2.1 or later.

---

## Quick Start

### 1. `summary`
```bash
nextflow run nw-page/bb-utils \
    -r main \
    --db s3://bucket/bigbacter_db \
    --mode summary
```

### 2. `remove`
Preview the removal with `--dry_run`, then run it again without the flag.
```bash
nextflow run nw-page/bb-utils \
    -r main \
    --db s3://bucket/bigbacter_db \
    --mode remove \
    --taxa Escherichia_coli \
    --cluster 12 \
    --samples sample1,sample2 \
    --dry_run
```

### 3. `push`
```bash
nextflow run nw-page/bb-utils \
    -r main \
    --db s3://bucket/bigbacter_db \
    --mode push \
    --run s3://bucket/bigbacter_results/1794182400
```

{: .warning}
Add `--dry_run` to `remove` and `push` modes to test a command before executing it.

---

## Parameters

|Parameter|Default|Modes|Description|
|:-|:-|:-|:-|
|`--db`| |all|BigBacter database|
|`--mode`| |all|`summary`, `remove` or `push`|
|`--outdir`|`bb_utils_results`|all|Where reports and manifests are saved|
|`--threads`|`16`|all|Number of list, copy and delete operations run at once|
|`--dry_run`|`false`|remove, push|Report what would happen and change nothing|
|`--taxa`| |all|`remove`: one taxon (required). `summary` and `push`: optional, comma-separated.|
|`--cluster`| |summary, remove|`remove`: one cluster. `summary`: optional, comma-separated.|
|`--samples`| |remove|Comma-separated sample names, or a file with one name per line. Requires `--cluster`.|
|`--added_after`| |remove|Remove samples added at or after this time|
|`--added_before`| |remove|Remove samples added before this time|
|`--all`|`false`|remove|Remove the whole taxon|
|`--prune_empty`|`true`|remove|Delete clusters left with no samples|
|`--run`| |push|BigBacter run directory (`${outdir}/${timestamp}`)|
|`--overwrite`|`false`|push|Replace sample files that are already in the database|
|`--allow_missing_sig`|`false`|push|Push samples that have no signature in the run|

---

## General Behavior

### Outputs
Each run writes its reports to `${outdir}/${unix_time}-${mode}/`. The default `--outdir` is `bb_utils_results`.

`remove` and `push` write a manifest listing every file they affect. The manifest is written before any file is deleted or copied, so there is a record even if the run is interrupted.

### Taxa names
Taxon names are handled in the same manner as BigBacter: 
1. Every character that is not a letter or number becomes an underscore (`_`) - e.g.,`"Escherichia coli" == Escherichia_coli`
2. Names are case sensitive - e.g., `"escherichia coli" != "Escherichia coli"`

---

## Mode: `summary`

```bash
nextflow run nw-page/bb-utils -r main --db <db> --mode summary
```

Limit the summary to one or more taxon / cluster using the `--taxa` and `--cluster` parameters (comma-separated lists).

### Outputs

|File|Description|
|:-|:-|
|`summary_taxa.tsv`|One row per taxon: clusters, samples, size, first and last added, and the `config.json` settings|
|`summary_clusters.tsv`|One row per cluster: samples, reference name, length and contigs, size, first and last added|
|`summary_samples.tsv`|One row per sample: taxon, cluster, when it was added, and which files it has|
|`summary_issues.tsv`|Problems found in the database|

### Issues reported

|Level|Issue|
|:-|:-|
|Taxon|`config.json` is missing or has no `clust_dist`|
|Cluster|`ref.fa.gz` or `ref.json.gz` is missing|
|Cluster|The cluster has no samples|
|Sample|The variant tarball, assembly, or signature is missing|
|Sample|A signature has no files in any cluster|
|Sample|The sample is in more than one cluster|

{: .note}
Signature files are not created for samples that have their cluster set manually in the BigBacter samplesheet.
---

## Mode: `remove`

Removals are always limited to one taxon (set with `--taxa`). 

Samples can be removed using on the following methods:

|Method|What is removed|
|:-|:-|
|`--cluster <name> --samples <a,b,c>`|The named samples in that cluster. `--samples` can also be a file with one name per line.|
|`--cluster <name>`|The whole cluster|
|`--added_after <time>` and / or `--added_before <time>`|Samples added in that window. Add `--cluster` to limit it to one cluster.|
|`--all`|The whole taxon, including `config.json`|

For each removed sample, its signature, assembly and variant tarball are deleted together.

{: .warning}
Deleted files cannot be recovered unless the storage location keeps versions (for example S3 bucket versioning).

### Removing by time
A sample's added time is the last-modified time of its variant tarball (`clusters/${cluster}/var/${sample}.tar.gz`).

Times can be given as Unix time in seconds (like BigBacter run timestamps), a date (`2026-11-09`), or a date and time (`2026-11-09T14:30:00`). They are read as UTC unless an offset is included. `--added_after` includes the time given; `--added_before` does not.

**Example:** remove everything added to the *E. coli* database on or after November 1, 2026
```bash
nextflow run nw-page/bb-utils \
    -r main \
    --db s3://bucket/bigbacter_db \
    --mode remove \
    --taxa Escherichia_coli \
    --added_after 2026-11-01
```

{: .important}
Last-modified times are reset when files are rewritten. If a database has been copied or synced to a new location, every sample will look like it was added on the day it was copied.

### Empty clusters
When a removal leaves a cluster with no samples, the cluster's reference and directory are deleted too. This is the default because [Floc](https://github.com/nw-page/floc) can reuse the name of an empty cluster for unrelated samples, which would then be compared against the old reference. Use `--prune_empty false` to bypass this default behavior.

### Outputs

|File|Description|
|:-|:-|
|`remove_manifest.tsv`|One row per file: taxon, cluster, sample, file type, path, size, last-modified time and status (`deleted`, `dry_run`, or `failed` with the reason)|

---

## Mode: `push`

`push` copies the database files of a BigBacter run into the database. It does the same job as running BigBacter with `--push true`. This provides an alternative method for pushing database files without needing to use the Nextflow `resume` feature.

```bash
nextflow run nw-page/bb-utils -r main --db <db> --mode push --run <outdir>/<timestamp>
```

`--run` is the timestamped directory of one BigBacter run. Use `--taxa` (comma-separated) to push only some of the taxa in the run.

{: .important}
> `push` mode is only compatible with BigBacter v2.2.1 and later. Earlier versions did not publishes a copy of all databases files to the `outdir`!

### Files copied

|Run directory (`${outdir}/${timestamp}/`)|Database (`${db}/`)|
|:-|:-|
|`${taxa}/config.json`|`${taxa}/config.json`|
|`${taxa}/sig/${sample}.sig.gz`|`${taxa}/sig/${sample}.sig.gz`|
|`${taxa}/${cluster}/asm/ref.fa.gz`|`${taxa}/clusters/${cluster}/asm/ref.fa.gz`|
|`${taxa}/${cluster}/asm/${sample}.fa.gz`|`${taxa}/clusters/${cluster}/asm/${sample}.fa.gz`|
|`${taxa}/${cluster}/aux/ref.json.gz`|`${taxa}/clusters/${cluster}/aux/ref.json.gz`|
|`${taxa}/${cluster}/var/${sample}.tar.gz`|`${taxa}/clusters/${cluster}/var/${sample}.tar.gz`|

Samples are only pushed if they contain a variant tarball in the run directory

### Checks
Anything that fails one of the checks below is skipped and reported

|Level|Skipped when|
|:-|:-|
|Taxon|`clust_dist` in the run's `config.json` differs from the database|
|Taxon|The database has the taxon but no `config.json`|
|Taxon|The taxon is new to the database and the run has no `config.json`|
|Cluster|The cluster is new to the database and the run has no `ref.fa.gz`|
|Cluster|The reference in the run differs from the reference in the database|
|Sample|The sample is already in the database under a different cluster|
|Sample|The sample's assembly or signature is missing from the run|

References and the `config.json` file are <u>never</u> replaced. 

{: .note}
- Samples will not be overwritten unless the `--overwrite` param is used.
- Samples whose cluster was set in the BigBacter samplesheet have no signature. Use `--allow_missing_sig` to push them.

{: .important}
Make sure you push each run before starting the next BigBacter run for the same taxon. Two runs that have not been pushed can each create a cluster with the same name from different samples. `push` detects this as a reference mismatch and skips the cluster.

### Outputs

|File|Description|
|:-|:-|
|`push_manifest.tsv`|One row per file: taxon, cluster, sample, file type, source, destination, size and status (such as `copied`, `dry_run`, or `skipped` or `failed` with the reason)|

The run exits with an error if any file could not be copied or if anything was skipped by a check, so skipped items are not missed in automated use.

---

{: .warning}
Do not run `remove` or `push` while a BigBacter run with `--push true` is writing to the same database. bb-utils does not lock the database.