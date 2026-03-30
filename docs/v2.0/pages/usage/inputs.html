---
title: Inputs
layout: page
nav_order: 4
grand_parent: v2.0
parent: Usage Guide
permalink: /docs/v2.0/pages/usage/inputs/
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
|`fastq_2`|Absolute path to the forward (R2) Illumina read file (`.fq` or `.fastq`). Must be supplied with `fastq_1`. Cannot be supplied with `sra` column.|
|`assembly`| |
|`taxon`| |
|`sra`||
|`genbank`| |
|`cluster`| |

## `--max_reads`
The maximum number of reads to include in the analysis.

- Options: `0...Inf`
- Default: `2_000_000`

> Samples with more than this number of reads will be randomly down-sampled using `seqtk sample`. Read counts are based on the sum of the forward and reverse reads.


## TODO

```
    // -------------------------------
    // Sample inputs
    // -------------------------------
    input                      = null    // Path to input samplesheet or data directory
    max_reads                  = 2_000_000 // Max number of reads per sample
    max_depth                  = 100       // Max depth per sample (impacts de novo assembly and variant calling)

    // -------------------------------
    // BigBacter database
    // -------------------------------
    db                         = 'bigbacter_db' // Path to surveillance database
    push                       = false          // Push outputs to database

    // -------------------------------
    // Assets
    // -------------------------------
    gambit_db                  = "${projectDir}/assets/databases/gambit"  // Gambit database for taxonomic classification
    microreact_template        = "$projectDir/assets/template.microreact" // Microreact template JSON for visualization

    // -------------------------------
    // Clustering
    // -------------------------------
    clust_dist                 = 0.03  // Distance threshold used to create clusters
    clust_min_hash_freq        = 0.05  // Minimum frequency for a hash to be included in the global hashes
    clust_min_hash_frac        = 0.5   // Minimum fraction of sample hashes shared with the global hashes after filtering
    clust_ignore_qc            = false // Ignore clustering QC results - include all samples and do not fail
    clust_overwrite            = false // Overwrite signature files if they already exist for a sample

    // -------------------------------
    // Reference selection
    // -------------------------------
    ref_min_contig_len         = 300  // Minimum contig length in reference
    ref_contig_penalty         = 0.2  // Contig penalty applied when selecting references (more contigs = worse score)
    ref_ksize                  = 31   // K-mer size used when comparing references
    ref_scaled                 = 100  // K-mer scaling factor used when comparing references

    // -------------------------------
    // Variant calling
    // -------------------------------
    min_genome_fraction        = 0.8  // Minimum genome fraction for a sample to be included in the core genome analysis
    min_core_fraction          = 0.9  // Minimum core genome fraction for a reference site to be included in the core genome analysis
    mask_recomb                = true // Perform recombination masking, in addition to standard variant detection

    // -------------------------------
    // Phylogenetic analysis
    // -------------------------------
    min_tree                   = 2    // Minimum number of samples in a core analysis needed to produce a tree (>1)
    strong_link_threshold      = 10   // Nucleotide threshold for defining strong linkages between samples (0 -> strong_link_threshold)
    inter_link_threshold       = 50   // Nucleotide threshold for defining intermediate linkages between samples (strong_link_threshold + 1 -> inter_link_threshold)
    partition_distance         = 100  // Nucleotide threshold for grouping samples into tree partitions
```
