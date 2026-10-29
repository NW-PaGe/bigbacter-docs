---
title: "BBv1 vs. BBv2: What Changes When You Switch"
layout: page
date: 2026-10-29
author: Jared Johnson
description: Two differences you may notice when moving from BigBacter v1 to v2, why they happen, and whether they matter.
nav_order: -20261029
---

# {{ page.title }}
{: .no_toc }

<small>{{ page.date | date: "%B %-d, %Y" }} · {{ page.author }}</small>

1. TOC
{:toc}

---

# Overview

BigBacter v1 (BBv1) and v2 (BBv2) produce **very similar clustering patterns** overall. Krista Miller from DCLS explored this in a couple of [posters](https://millerkrista.github.io/_pages/asm-big-2026.html) comparing the two versions.

There are two areas where you may notice a difference after switching:

|#|What you might see|Why|Is it a problem?|
|:-|:-|:-|:-|
|1|More SNP differences between samples, and some polytomies becoming bifurcations|BBv2 uses a **soft-core genome** (sites present in ≥ 90% of samples) instead of a strict core (100%)|**Unlikely.** This is intended and gives better resolution. See [how to check](#when-can-ambiguous-sites-have-a-bigger-impact) for the rare cases where it matters.|
|2|A handful of SNPs (sometimes > 10) between the reference sample and its own assembly|BBv2 now **reports which sample was used as the reference**, which makes an existing mapping artifact visible|**Known issue.** Not new in BBv2, and we are working on a fix.|

---

# 1. A soft-core genome instead of a strict core

{: .important}
> **What changed:** BBv1 included a site in the core genome only if **100%** of samples had a real base call (not `N`) there. BBv2 includes a site if at least **90%** of samples do.

Requiring every sample to have a base call means a single low-coverage sample can remove a site from the comparison for everyone. Relaxing this to 90% keeps more of the genome in the analysis.

{: .tip}
> Want BBv1 behavior? Run BBv2 with `--min_core_fraction 1.0`. See [`--min_core_fraction`]({{ site.baseurl }}/docs/v2.0/pages/inputs/#--min_core_fraction) for details.

## Impact: more SNP differences

You will likely see **higher pairwise SNP distances** in BBv2 than in BBv1 for the same samples.

{: .note}
> This is the intended behavior. A larger core genome means more sites are compared, so more of the true differences between samples are detected. The result is greater resolution, not less similarity.

## Impact: polytomies may become bifurcations

A **polytomy** is a node in the tree where three or more samples branch from the same point, meaning the data can't tell which of them are most closely related. In BBv2, some of these may resolve into a **bifurcation** (a node that splits into exactly two branches).

![Side-by-side trees. In BBv1, samples A, B and C all split from one node. In BBv2, A and B are joined by an extra, very short branch.]({{ site.baseurl }}/assets/media/blog/polytomy-to-bifurcation.svg)

**Why this happens:** the soft-core genome now includes sites where a few samples have an ambiguous (`N`) base. Maximum likelihood programs like IQ-TREE don't allow branches to be exactly zero, so these ambiguous sites can produce **very short branches** that split a polytomy into two.

BigBacter runs IQ-TREE with the `-czb` flag **by default**. This flag collapses branches at or near IQ-TREE's minimum branch length back into polytomies, which removes most of these artificial splits. Some short branches can still remain, however. In practice, we have observed **very small branch lengths (< 1 estimated nucleotide substitution) between samples with 0 SNP differences but thousands of ambiguous sites**.

{: .note}
> **We do not anticipate this being a problem.** These branches should be short, normally **less than 1 estimated nucleotide substitution**, and shouldn't change the overall relationships between samples. If you observe a situation where this does cause an issue, please [submit an issue on GitHub](https://github.com/nw-page/bigbacter/issues).

### When can ambiguous sites have a bigger impact?

There are some circumstances where ambiguous sites can bias a tree, but this is **unlikely in most cases**. Simulation studies ([Lemmon et al. 2009](https://academic.oup.com/sysbio/article/58/1/130/1677143)) show the effect is strongest when:

- **The same group of samples is ambiguous at many sites**, for example several samples that share a low-coverage region. Ns scattered across different samples tend to cancel out.
- **The relationship has little real SNP support**, such as samples separated by only 0–2 SNPs. Relationships supported by real SNPs generally hold up.
- **Ambiguous sites cluster in regions that evolve at a different rate** than the rest of the genome, which can distort branch lengths.

{: .tip}
> **Check for discrepancies by comparing pairwise SNP distances with tree branch lengths.**
>
> - **Pairwise SNP distances** (`*_snp-dist.csv`) are always calculated using only the sites where *both* samples have a base call. Sites with an N in either sample are skipped, and Ns in other samples have no effect.
> - **Tree branch lengths** (`*.nwk`) are estimated from the whole alignment, including ambiguous sites, and are reported in estimated nucleotide substitutions.
>
> For a pair of samples, the distance along the tree (the sum of the branch lengths between them) should be close to their pairwise SNP distance. **A large difference between the two suggests ambiguous sites may be distorting the tree.** If you see one, rerun with `--min_core_fraction 1.0` to check whether the result persists, and please [let us know](https://github.com/nw-page/bigbacter/issues).

---

# 2. The reference sample is now reported

{: .important}
> **What changed:** BBv2 now tells you which sample was selected as the reference genome for each cluster (see [Reference Selection]({{ site.baseurl }}/docs/v2.0/pages/overview/#reference-selection)).

Because the reference is a de novo assembly of one of the samples, you might expect that sample to show **zero SNPs** when its reads are mapped back to its own assembly. In practice, you may see a **moderate number of SNPs (sometimes more than 10)**.

## Why this happens

Bacterial genomes contain **repeated regions**, such as paralogs (duplicated genes) and other repeats. These copies are often nearly, but not perfectly, identical. Short-read assemblers frequently **collapse** them into a single copy in the assembly.

When reads are mapped back to that assembly, reads from *every* copy are forced onto the one region that exists. Wherever the copies differ, the reads disagree with the reference, and those positions get called as SNPs.

{: .example}
> [Ribeiro et al. (2015)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-015-0801-z) saw exactly this. They mapped reads back to de novo assemblies of the same genome the reads came from and still found false SNPs. Most of the reads supporting those SNPs were mismapped, and the authors traced the cause to repeats and paralogs that were collapsed or missing in the assembly. Mapping back to the complete original genome produced far fewer false SNPs.

![Diagram. The sample genome has two slightly different copies of a repeat. The assembly contains only one copy. Reads from both copies pile onto that region, and the bases where Copy 2 differs are called as SNPs.]({{ site.baseurl }}/assets/media/blog/collapsed-repeat-mapping.svg)

## What this means for you

{: .warning}
> This is a **real issue** that we are actively working to address. These inflated SNP counts can affect any sample with reads in collapsed repeat regions, not just the reference sample.

{: .note}
> **This is not new behavior.** The same artifact was present in BBv1. BBv2 simply makes it visible by reporting the reference sample, so you may notice it for the first time without anything having changed.

---

# Further reading

- Lemmon, A. R., Brown, J. M., Stanger-Hall, K., & Lemmon, E. M. (2009). [The effect of ambiguous data on phylogenetic estimates obtained by maximum likelihood and Bayesian inference](https://academic.oup.com/sysbio/article/58/1/130/1677143). *Systematic Biology*, 58(1), 130–145.
- Ribeiro, A., et al. (2015). [An investigation of causes of false positive single nucleotide polymorphisms using simulated reads from a small eukaryote genome](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-015-0801-z). *BMC Bioinformatics*, 16, 382.

---

# Questions?

If you're seeing differences between BBv1 and BBv2 that aren't explained here, please [open an issue](https://github.com/nw-page/bigbacter/issues) or reach out to the BigBacter team. We're happy to set up a time to talk through your results.
