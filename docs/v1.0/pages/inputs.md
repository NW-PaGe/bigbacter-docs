---
title: Inputs
layout: page
nav_order: 4
parent: v2.0
permalink: /docs/v2.0/pages/inputs/
---

# {{ page.title }}
{: .no_toc}

1. TOC
{:toc}

---

# Overview
Pipeline parameters can be adjusted using the following methods:

1. At the command line using `--{parameter_name}` (e.g., `--input`)
2. In the `nextflow.config` file
3. In a JSON file via the `-params-file` parameter

It is also possible to pass arguments directly to a pipeline process using the `ext.args` variable in `conf/modules.config` (see example below):
```
    withName: 'IVAR_CONSENSUS' {
        ext.args            = "-n 'N' -k"
        ext.when            = {  }
        publishDir = [
            [
                path: { "${params.outdir}/${meta.id}/assembly/" },
                pattern: "none",
                mode: 'copy'
            ],
            [
                path: { "${params.outdir}/${meta.id}/qc" },
                pattern: "*.csv",
                mode: 'copy'
            ]
        ]
    }
```

---

# Input Options

## `--input`
Path to the samplesheet.

### Example samplesheet
`samplesheet.csv`:
```
sample,fastq_1,fastq_2
sample01,sample01_R1_001.fastq.gz,sample01_R2_001.fastq.gz
sample02,sample02_R1_001.fastq.gz,sample02_R2_001.fastq.gz
```

### Samplesheet columns

{: .note}
- Required columns: `sample`, and `fastq_1` + `fastq_2` or `sra`
- All file paths in the samplesheet must be absolute.

|Column Name|Description|
|:-|:-|
|`sample`|Sample name|
|`fastq_1`|Absolute path to the forward (R1) Illumina read file (`.fq` or `.fastq`). Must be supplied with `fastq_2`. Cannot be supplied with `sra` column.|
|`fastq_2`|Absolute path to the reverse (R2) Illumina read file (`.fq` or `.fastq`). Must be supplied with `fastq_1`. Cannot be supplied with `sra` column.|
|`assembly`|Absolute path to an existing assembly file (`.fasta` or `.fa`). If provided, assembly will be skipped for this sample.|
|`taxa`|Taxonomic name of the sample (e.g., `Staphylococcus aureus`). If provided, taxonomic classification will be skipped for this sample.|
|`sra`|SRA accession number (e.g., `SRR12345678`). Cannot be supplied with `fastq_1` or `fastq_2` columns.|
|`genbank`|GenBank accession number of a reference genome to use for this sample. Overrides automatic reference selection.|
|`cluster`|Pre-assigned cluster ID for this sample. If provided, cluster assignment will be skipped for this sample.|

## `--max_reads`
The maximum number of reads to include in the analysis.

- Options: `0...Inf`
- Default: `2_000_000`

> Samples with more than this number of reads will be randomly down-sampled using `seqtk sample`. Read counts are based on the sum of the forward and reverse reads.

## `--max_depth`
The maximum sequencing depth per sample.

- Options: `0...Inf`
- Default: `100`

> Impacts de novo assembly and variant calling. Samples exceeding this depth will be down-sampled prior to these steps.

---

# Database Options

## `--db`
Path to the BigBacter surveillance database.

- Default: `bigbacter_db`

> This database stores signatures, cluster assignments, and other persistent outputs across runs.

## `--push`
Whether to push results to the BigBacter database after the run.

- Options: `true`, `false`
- Default: `false`

> When enabled, results are written to `--db` so they are included in future runs. Commonly used with `--resume` to push results from a previous run without recomputing them.

---

# Asset Options

## `--gambit_gdb`
Path to the GAMBIT database file used for taxonomic classification.

- Default: `https://storage.googleapis.com/jlumpe-gambit/public/databases/refseq-curated/1.0/gambit-refseq-curated-1.0.gdb`

> Used to classify samples when no `taxa` is provided in the samplesheet.

## `--gambit_gs`
Path to the GAMBIT database file used for taxonomic classification.

- Default: `https://storage.googleapis.com/jlumpe-gambit/public/databases/refseq-curated/1.0/gambit-refseq-curated-1.0.gs`

> Used to classify samples when no `taxa` is provided in the samplesheet.

## `--microreact_template`
Path to the Microreact template JSON file used for visualization.

- Default: `${projectDir}/assets/template.microreact`

---

# Clustering Options

## `--clust_dist`
Distance threshold used to define clusters.

- Options: `0...1`
- Default: `0.03`

> Samples with a pairwise distance below this threshold will be assigned to the same cluster.

## `--clust_min_hash_freq`
Minimum frequency for a hash to be included in the global hash set.

- Options: `0...1`
- Default: `0.05`

> Hashes occurring below this frequency across all samples are excluded from the global reference set.

## `--clust_min_hash_frac`
Minimum fraction of sample hashes that must overlap with the global hash set after filtering.

- Options: `0...1`
- Default: `0.5`

> Samples falling below this threshold may indicate low-quality or divergent sequences.

## `--clust_ignore_qc`
Whether to ignore clustering QC results and include all samples regardless of QC status.

- Options: `true`, `false`
- Default: `false`

> When enabled, samples that would otherwise fail clustering QC are still included in the analysis.

## `--clust_overwrite`
Whether to overwrite existing signature files for a sample.

- Options: `true`, `false`
- Default: `false`

> By default, signature files are reused if they already exist in `--db`. Enable this to force regeneration.

## `--clust_plot`
Whether to create PCoA and Neighbor-joining plots when running floc.

- Options: `true`, `false`
- Default: `false`

> This can be helpful for interpreting cluster relationships. May take a significant amount of time when there are many samples!
---

# Reference Selection Options

## `--ref_min_contig_len`
Minimum contig length (bp) allowed in a reference genome.

- Options: `0...Inf`
- Default: `300`

> Contigs shorter than this value are excluded from the reference prior to analysis.

## `--ref_contig_penalty`
Penalty applied to references with more contigs during reference selection scoring.

- Options: `0...1`
- Default: `0.2`

> Higher values more strongly penalize fragmented references. A score of `0` applies no penalty.

## `--ref_ksize`
K-mer size used when comparing references.

- Options: `0...Inf`
- Default: `31`

## `--ref_scaled`
K-mer scaling factor used when comparing references.

- Options: `0...Inf`
- Default: `100`

> Higher values reduce memory usage at the cost of resolution. Used by the sourmash sketching step.

---

# Variant Calling Options

## `--min_genome_fraction`
Minimum fraction of the reference genome that must be covered for a sample to be included in core genome analysis.

- Options: `0...1`
- Default: `0.8`

> Samples falling below this threshold are excluded from variant calling and downstream phylogenetic analysis.

## `--min_core_fraction`
Minimum fraction of samples that must have coverage at a reference site for it to be included in the core genome.

- Options: `0...1`
- Default: `0.9`

> Sites with coverage in fewer samples than this threshold are excluded from the core genome alignment.

## `--mask_recomb`
Whether to perform recombination masking in addition to standard variant detection.

- Options: `true`, `false`
- Default: `true`

> When enabled, recombinant regions identified by Gubbins are masked prior to phylogenetic analysis.

## `--keep_bam`
 Keep the bam file created during variant calling.

- Options: `true`, `false`
- Default: `false`

> Enabling will dramatically increase database size.

---

# Phylogenetic Analysis Options

## `--min_tree`
Minimum number of samples required in a core genome analysis to produce a phylogenetic tree.

- Options: `2...Inf`
- Default: `2`

> Must be greater than 1. Clusters with fewer samples than this value will not have a tree generated.

## `--strong_link_threshold`
Upper nucleotide distance threshold for defining a strong linkage between two samples.

- Options: `0...Inf`
- Default: `10`

> Sample pairs with SNP distances from `0` to this value are classified as strongly linked.

## `--inter_link_threshold`
Upper nucleotide distance threshold for defining an intermediate linkage between two samples.

- Options: `0...Inf`
- Default: `50`

> Sample pairs with SNP distances from `--strong_link_threshold + 1` to this value are classified as intermediately linked.

## `--partition_distance`
Nucleotide distance threshold for grouping samples into tree partitions.

- Options: `0...Inf`
- Default: `100`

> Samples within this SNP distance of one another are grouped into the same partition for visualization.