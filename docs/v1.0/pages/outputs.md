---
title: Output
layout: page
nav_order: 5
parent: v1.0
permalink: /docs/v1.0/pages/output/
---

# {{ page.title }}
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## All Outputs

```
${outdir}
└── ${timestamp}
    ├── ${taxa}
    │   ├── ${cluster}
    │   │   ├── alns
    │   │   │   └── ${timestamp}-${taxa}-${cluster}.{gubbins,snippy}.aln
    │   │   ├── dists
    │   │   │   └── ${timestamp}-${taxa}-${cluster}-{accessory,core-snps}_.{poppunk,gubbins,snippy}-{long,wide}.csv
    │   │   ├── figures
    │   │   │   ├── ${timestamp}-${taxa}-${cluster}-core-snps_{ML,NJ}.{gubbins,snippy}.microreact
    │   │   │   ├── ${timestamp}-${taxa}-${cluster}-core-snps_{ML,NJ}.{gubbins,snippy}.jpg
    │   │   │   └── ${timestamp}-${taxa}-${cluster}-{accessory,core-snps}_dist.{poppunk,gubbins,snippy}.jpg
    │   │   ├── snippy
    │   │   │   └── ${timestamp}-${species}-${sample}.tar.gz
    │   │   ├── stats
    │   │   │   └── ${timestamp}-${species}-${sample}.{gubbins,snippy}.stats
    │   │   └── trees
    │   │       └── ${timestamp}-${taxa}-${cluster}-core-snps_{ML,NJ}.{gubbins,snippy}.nwk
    │   ├── poppunk
    │   │   ├── ${timestamp}-${species}-pp_core_NJ.nwk
    │   │   ├── ${timestamp}-${species}-pp_microreact_clusters.csv
    │   │   ├── ${timestamp}-${species}-pp_perplexity20.0_accessory_mandrake.dot
    │   │   ├── ${timestamp}-${species}-pp.microreact
    │   │   ├── ${timestamp}-${species}-pp-core-acc-dist.txt.gz
    │   │   ├── ${timestamp}-${species}-pp-jaccard-dist.txt.gz
    │   │   └── ${timestamp}-${species}-pp-clusters.csv
    │   ├── other
    │   │   ├── multiqc_report.html
    │   │   └── software_versions.yml
    │   └── ${timestamp}-summary.tsv
    └── ${timestamp}-db-info.csv
```

## Run Summary

Results are summarized for all samples included in the analysis. This includes both new samples and those that were stored in your BigBacter database. Subsets of this summary are also saved for each species-cluster.

```
${timestamp}-summary.tsv
${timestamp}-${species}-${cluster}-summary.csv
```

Column descriptions are provided below.

| Column Name | Description |
|:---|:---|
| `ID` | Sample ID (`_T[0-9]+` denotes replicate number) |
| `STATUS` | Sample status (`NEW` or `OLD`) |
| `QUAL` | Sample quality status (`PASS` or `FAIL`). Based on values in `PER_GENFRAC`, `PER_HET`, and `PER_LOWCOV` |
| `RUN_ID` | Run timestamp |
| `TAXA` | Sample taxonomy (same as supplied in the samplesheet via `taxa`) |
| `CLUSTER` | Assigned PopPUNK cluster |
| `ISO_IN_CLUSTER` | Total number of isolates in the assigned PopPUNK cluster |
| `ISO_PASS_QC` | Number of isolates in the assigned PopPUNK cluster that passed QC |
| `MEAN_SNP_DIST_SNIPPY` | Mean pairwise SNP distance between the sample and all other isolates in the assigned cluster that passed QC, including the reference (without recombination masked) |
| `MIN_SNP_DIST_SNIPPY` | Minimum pairwise SNP distance, as above (without recombination masked) |
| `MAX_SNP_DIST_SNIPPY` | Maximum pairwise SNP distance, as above (without recombination masked) |
| `STRONG_LINKAGE_SNIPPY` | List of samples in the cluster with pairwise SNP differences ≤ `--strong_link_cutoff` (without recombination masked) |
| `INTER_LINKAGE_SNIPPY` | List of samples in the cluster with pairwise SNP differences between `--strong_link_cutoff` and `--inter_link_cutoff` (without recombination masked) |
| `MEAN_SNP_DIST_GUBBINS` | Mean pairwise SNP distance, as above (with recombination masked) |
| `MIN_SNP_DIST_GUBBINS` | Minimum pairwise SNP distance, as above (with recombination masked) |
| `MAX_SNP_DIST_GUBBINS` | Maximum pairwise SNP distance, as above (with recombination masked) |
| `STRONG_LINKAGE_GUBBINS` | List of samples in the cluster with pairwise SNP differences ≤ `--strong_link_cutoff` (with recombination masked) |
| `INTER_LINKAGE_GUBBINS` | List of samples in the cluster with pairwise SNP differences between `--strong_link_cutoff` and `--inter_link_cutoff` (with recombination masked) |
| `LENGTH` | Length of the reference genome (bp) |
| `ALIGNED` | Reference positions covered by the sample (bp) |
| `UNALIGNED` | Reference positions not covered by the sample (bp) |
| `RECOMB` | Number of sites in recombinant regions, including variant and invariant sites (bp) |
| `VARIANT` | Number of variant sites detected in the sample, as compared to the reference (bp) |
| `HET` | Number of heterogeneous sites (bp) |
| `MASKED` | Number of masked sites (bp) |
| `LOWCOV` | Number of low coverage sites (bp) |
| `PER_GENFRAC` | Percentage of the reference genome covered by the sample |
| `PER_LOWCOV` | Percentage of the reference genome with low coverage sites |
| `PER_HET` | Percentage of the reference genome with heterogeneous sites |

## PopPUNK Results (`poppunk/`)

### PopPUNK Visualizations

Visualizations of the PopPUNK database are generated via `poppunk_visualise` with the `--microreact` option. You can view the `.microreact` file at [https://microreact.org/upload](https://microreact.org/upload).

```
${timestamp}-${species}-pp_core_NJ.nwk
${timestamp}-${species}-pp_microreact_clusters.csv
${timestamp}-${species}-pp_perplexity20.0_accessory_mandrake.dot
${timestamp}-${species}-pp.microreact
```

### PopPUNK Clusters

Cluster assignments for all samples in the PopPUNK database. Should contain the same information as `${timestamp}-${species}-pp_microreact_clusters.csv`.

```
${timestamp}-${species}-pp-clusters.csv
```

### PopPUNK Distances

Pairwise core/accessory distances and Jaccard distances (same as Mash) produced from the PopPUNK database using `sketchlib query`.

```
${timestamp}-${species}-pp-core-acc-dist.txt.gz
${timestamp}-${species}-pp-jaccard-dist.txt.gz
```

## Alignment Files (`alns/`)

Whole genome (Snippy) or core genome (Gubbins) alignment files.

```
${timestamp}-${taxa}-${cluster}.{gubbins,snippy}.aln
```

## Pairwise Distances (`dists/`)

Pairwise distance files in long and wide formats. Included for core SNPs (Snippy and Gubbins) and accessory distances.

```
${timestamp}-${taxa}-${cluster}-{accessory,core-snps}_.{poppunk,gubbins,snippy}-{long,wide}.csv
```

## Figures (`figures/`)

Static image files (`.jpg`) and Microreact files of pairwise distance matrices and/or phylogenetic trees.

```
${timestamp}-${taxa}-${cluster}-core-snps_{ML,NJ}.{gubbins,snippy}.jpg
${timestamp}-${taxa}-${cluster}-{accessory,core-snps}_dist.{poppunk,gubbins,snippy}.jpg
```

{: .note }
> In static images, new samples are shown in bold, black text. Historic samples are shown in grey, plain text. Asterisks on nodes indicate bootstrap values < 70%.

## Individual SNP Files (`snippy/`)

Tar files containing all the information needed to perform SNP analysis using `snippy-core`.

```
${timestamp}-${species}-${sample}.tar.gz
```

## Analysis Statistics (`stats/`)

Sample statistics for Snippy and Gubbins.

```
${timestamp}-${species}-${sample}.{gubbins,snippy}.stats
```

## Phylogenetic Trees (`trees/`)

Maximum likelihood or neighbor-joining trees generated from Snippy or Gubbins core SNP alignments.

```
${timestamp}-${taxa}-${cluster}-core-snps_{ML,NJ}.{gubbins,snippy}.nwk
```

## Database Info

Snapshot of your BigBacter database. This is only generated if `--db_info` is `true`.

```
${timestamp}-db-info.csv
```