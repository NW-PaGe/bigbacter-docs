---
title: Overview
layout: page
nav_order: 3
parent: v2.0
permalink: /docs/v2.0/pages/overview/
---

# {{ page.title }}
{: .no_toc }

1. TOC
{:toc}

---

# What is BigBacter?

BigBacter is a Nextflow pipeline for routine bacterial genomic surveillance. It accepts raw reads or assemblies, clusters samples by genomic similarity, constructs core genome alignments, and produces phylogenetic trees and pairwise distance matrices — all in an iterative, database-backed workflow designed to grow with your dataset over time.

## Key Features

<div style="padding: 1em; margin: 1em 0;">

🧬 <strong>Iterative clustering</strong> — cluster assignments stay consistent across runs using a per-sample sourmash database that expands automatically with each new submission<br>
🧬 <strong>Soft-core phylogenomics</strong> — retains substantially more phylogenetic signal than strict-core approaches by tolerating a configurable level of missing data<br>
🧬 <strong>Automated reference selection</strong> — selects the most representative assembly per cluster using k-mer containment and assembly quality scoring; reuses the same reference on subsequent runs for consistent SNP distances<br>
🧬 <strong>Dual distance metrics</strong> — reports both core-genome SNP distances and whole-genome containment scores to capture both SNP-level and accessory genome variation<br>

</div>

---

# Inputs

## Read Processing

Reads can be supplied as FASTQ files (`fastq_1` / `fastq_2` columns) or downloaded automatically from NCBI using an SRA accession (`sra` column). Files exceeding the maximum read count set by `max_reads` (default: `2_000_000`) will be randomly subsampled using [seqtk](https://github.com/lh3/seqtk). All reads are then quality filtered using [fastp](https://github.com/opengene/fastp). If no reads are supplied, they will be derived from the genome assembly — read more [here](https://github.com/tseemann/snippy#finding-snps-between-contigs).

{: .important }
SNPs called from genome assemblies are considerably less reliable than those called from reads ([Wick et al., 2025](https://www.microbiologyresearch.org/content/journal/acmi/10.1099/acmi.0.001025.v3)). Genome assemblers prioritize contiguity and completeness over base-level accuracy, meaning assembly errors can be indistinguishable from true variants. Unlike read-based variant calling, there is no per-site depth or quality information available to scrutinize the confidence of a call. Samples where reads are unavailable should be interpreted with caution, particularly in outbreak investigations where a small number of SNPs may be the basis for epidemiological conclusions.

## Genome Assembly

Genome assemblies can be supplied as FASTA files (`assembly` column) or downloaded automatically from NCBI using a GenBank accession (`genbank` column). If no assembly is supplied, one will be created using [shovill](https://github.com/tseemann/shovill).

## Taxonomy

Sample taxonomy is supplied via the `taxa` column. Samples are split into taxon-specific groups prior to cluster and core genome analysis. Species-level classification is appropriate for most cases — e.g., *Escherichia coli*.

If no taxonomy is provided, BigBacter will automatically assign species-level taxonomy using [GAMBIT](https://github.com/jlumpe/gambit). GAMBIT uses k-mer based genome signatures to rapidly classify bacterial isolates. Automatically assigned taxonomy is subject to the limitations of GAMBIT's reference database — for novel or poorly represented species, manual review of the assigned taxonomy is recommended before proceeding.

{: .important }
BigBacter does not perform extensive quality checks on genome assemblies or taxonomy assignments. It is strongly recommended that assemblies and taxonomy are generated and validated upstream using a dedicated workflow with robust QC — e.g., [PHoeNIx](https://github.com/CDCgov/phoenix), [TheiaProk](https://public-health-bacterial-genomics-theiagen.readthedocs.io/en/latest/theiaprok.html), or [Bactopia](https://github.com/bactopia/bactopia).

---

# Clustering

Samples are clustered within each taxonomic group using [floc](https://github.com/DOH-JDJ0303/floc). Floc was developed at WA PHL for iterative sample clustering, accomplished using the sourmash [containment method](https://sourmash.readthedocs.io/en/latest/api.html#sourmash.MinHash.contained_by). This allows for a rough estimation of how much of the genome is shared between samples or between samples and existing clusters.

## How Clustering Works

Each time BigBacter is run, newly assigned cluster information is saved to a database. The next time BigBacter is run for the same species, this database is automatically loaded so that new samples can be placed relative to all previously observed clusters. This iterative approach means that cluster assignments remain consistent over time.

## Database Design

The floc database is intentionally simple compared to PopPUNK databases. Rather than storing cluster information in a single monolithic structure, floc saves data on a **per-sample basis**. This has several practical advantages:

- Individual samples can be **removed** from the database without rebuilding it from scratch (e.g., to exclude a contaminated or misidentified sample)
- Existing entries can be **modified** independently
- The database grows incrementally with each run, requiring no upfront preparation

A key consequence of this design is that BigBacter can be run with **as little as a single sample** for a given species. Databases are created on the fly during the first run and expanded with each subsequent run. This contrasts with PopPUNK, which requires a pre-built reference database to be created *a priori* before any samples can be assigned to clusters — a significant barrier when working with less common or emerging pathogens.

## Clustering Performance

[Kristen et al. 2026](https://millerkrista.github.io/_pages/aphl26poster_supp_materials.html) found that floc generally performs as well as or better than PopPUNK for cluster assignments, supporting the decision to adopt it as the clustering backbone for BigBacter v2.

{: .important }
> Databases created using BigBacter v1 are not compatible with v2.

---

# Core Genome Analysis

## Reference Selection

A reference genome is automatically selected for each cluster using [`bigbacter_select_ref.py`](https://github.com/DOH-JDJ0303/bigbacter-nf/blob/dev_2.0/bin/bigbacter_select_ref.py). When a cluster contains multiple assemblies, the script evaluates each one and selects the candidate that best represents the full genomic diversity of the group.

The selection process works as follows:

1. Contigs shorter than a minimum length (default: `300` bp) are filtered out.
2. A [MinHash sketch](https://sourmash.readthedocs.io/en/latest/) is built for each assembly using sourmash (default: `ksize=31`, `scaled=100`).
3. A **global sketch** is created by merging all per-assembly sketches, representing the total k-mer diversity across all candidates.
4. Each assembly is scored using the formula:

   ```
   score = containment × length / (n_contigs ^ penalty)
   ```

   Where `containment` measures what fraction of the global k-mer diversity is captured by the assembly, `length` rewards more complete assemblies, and the contig `penalty` (default: `0.2`) discourages fragmented assemblies. The assembly with the highest score is selected as the reference.

5. The selected reference is written to `ref.fa.gz` along with a metadata file (`ref.json`) recording the sample name, genome length, and contig count.

The selected reference is **saved to the BigBacter database** for the cluster. On subsequent runs, if a reference already exists in the database for a given cluster, it is reused rather than re-selected. This ensures that all samples within a cluster are always mapped against the same reference, keeping SNP distances and alignments consistent over time. A new reference is only selected when a cluster is being processed for the first time.

## Defining the Core Genome

Core genome analysis is performed using [polycore](https://github.com/DOH-JDJ0303/polycore). The process begins by mapping all samples in the cluster against the selected reference using [Snippy](https://github.com/tseemann/snippy), which generates per-sample alignments.

Rather than using a strict core — which requires data to be present in **every** sample at every site — BigBacter uses a **soft core** approach. As described by [Taouk et al. (2025)](https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.001346), strict cores can shrink dramatically as sample size and genome diversity increase, discarding potentially informative data. A soft core tolerates some missing data by applying a threshold: a site is included in the core genome if data are present in at least *N*% of samples (configurable; default targets the soft core). This preserves substantially more phylogenetic signal — in one benchmark of 10,000 *Salmonella* Typhi genomes, a 95% soft core retained ten times more informative sites than a 100% strict core.

To further improve alignment quality, polycore adds samples **progressively by genome fraction size** — larger, more complete assemblies are incorporated first. Samples that fall below the minimum genome size threshold are automatically excluded from core genome analysis, preventing low-quality assemblies from artificially eroding the core.

The per-sample SNP files generated by Snippy are **saved to the BigBacter database** on a per-sample basis. On subsequent runs, previously processed samples do not need to be re-mapped — their SNP files are retrieved directly from the database and combined with any newly mapped samples before the core genome is defined. This makes incremental runs substantially faster and means that adding new samples to an existing cluster only requires mapping the new samples rather than reprocessing the entire cluster from scratch.

## Calling Variants

Variants are called by polycore directly from the soft-core genome alignment, producing a SNP alignment used for all downstream phylogenetic and distance analyses.

For clusters large enough to warrant recombination masking, a **masked alignment** is also generated using [Gubbins](https://github.com/nickjcroucher/gubbins). Gubbins identifies genomic regions consistent with horizontal gene transfer or recombination and masks them, so that inferred phylogenies and SNP distances reflect vertical inheritance rather than recombination noise.

---

# Phylogenetic Analysis

## Core SNP Tree

A maximum likelihood tree is inferred using [IQ-TREE2](http://www.iqtree.org/) under the **GTR+I+G** model (general time reversible with a proportion of invariable sites and a discrete Gamma model for rate variation), with 1,000 rounds of rapid bootstrapping. While IQ-TREE2 supports automated model selection via ModelFinder, this can be prohibitively slow for routine surveillance. A standardized model was therefore selected based on published [recommendations](https://www.nature.com/articles/s41467-019-08822-w).

**Ascertainment bias correction** is applied via `-fconst` using the count of constant sites determined by polycore. This corrects for the fact that only variable sites are included in the SNP alignment, which would otherwise distort branch length estimates. Branch lengths are subsequently rescaled from substitutions per site to **estimated nucleotide substitutions** using the reference genome length.

To provide interpretable resolution across multiple scales of relatedness, trees are **partitioned into sub-trees** based on estimated pairwise nucleotide substitutions using DBSCAN (default threshold: `100` substitutions). This allows fine-scale outbreak investigation and broader population-level context to be viewed together.

## Pairwise Distances

Two complementary distance metrics are calculated for each cluster.

**Pairwise SNP distances** are computed by polycore from the soft-core genome alignment. These provide a core-genome view of genomic similarity and are the primary metric for outbreak detection and cluster confirmation.

**Pairwise genome containment** is calculated by floc within each cluster using sourmash k-mer sketches. This metric extends beyond the core genome to capture **accessory genome** differences — structural variation, gene gain/loss, and mobile elements that SNP-based methods miss entirely. The two metrics therefore complement each other and should be interpreted together.

{: .important }
Containment distances are based on exact k-mer matches, which can cause them to both **overestimate** accessory differences in variable core regions and **underestimate** accessory differences in repetitive regions or paralogs. Interpret with caution!

---

# Summary Report

Results are summarized at the taxon-cluster level in an interactive [Microreact](https://microreact.org) report. Each report includes:

- A maximum likelihood phylogenetic tree with bootstrap support
- Core and accessory genome pairwise distance matrices
- A genomic linkage summary for rapid identification of closely related samples
- A progressive core genome degradation plot illustrating how the soft-core genome shrinks as samples are added, which can be used to assess the impact of low-quality assemblies on the analysis

{: .note }
For a full description of report contents and how to interpret them, see the [Outputs](../outputs/results/) page.