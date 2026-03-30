---
title: Getting Started
layout: page
nav_order: 2
grand_parent: v2.0
parent: Usage Guide
permalink: /docs/v2.0/pages/usage/getting_started/
---

# {{ page.title }}
{: .no_toc}

1. TOC
{:toc}

# Dependencies
BigBacter is built using [Nextflow](https://www.nextflow.io/). Nextflow simplifies the development and execution of complex, scalable data analysis workflows by enabling reproducibility, portability across computing environments, and seamless integration with container technologies like Docker and Singularity.

The following are required to run BigBacter:
- [Nextflow](https://www.nextflow.io/docs/latest/install.html) (version 23.04.0 or higher)
- One of the following container engines: 
    - [Podman](https://podman.io/docs/installation) (recommended)
    - [Docker](https://docs.docker.com/engine/install/)
    - [Apptainer](https://apptainer.org/docs/admin/main/installation.html)
    - [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html). 

{: .important}
BigBacter does not support Conda / Mamba. Please submit a [feature request](https://github.com/DOH-JDJ0303/BigBacter/issues) if this is essential for your lab.

# Nextflow Basics
Below are some general pointers for how to run Nextflow workflows.
## Specifying the workflow version
There are two general ways you can specify which version of BigBacter you want to run:
1. Tell Nextflow which version you want to use

    ```bash
    nextflow run doh-jdj0303/BigBacter \
        -r v1.0 \
        -profile docker \
        --input samplesheet.csv \
        --outdir results
    ```

2. Clone the workflow version manually
    ```bash
    git clone https://github.com/doh-jdj0303/BigBacter.git -b v1.0 
    ```
    ```bash
    nextflow run BigBacter/main.nf \
        -profile docker \
        --input samplesheet.csv \
        --outdir results
    ```

{: .tip}
Nextflow caches repos in ~/.nextflow/assets/ by default. Removing this cache can be helpful when running into version-related issues.

## Specifying resource limits
We recommend adjusting the maximum resource limits that Nextflow can use. Setting these limits too high will cause the workflow to fail. This can be accomplished in the config file supplied via the `-c` paramater (see below).

{: .important}
Nextflow no longer allows resource limits to be specified from command line (e.g., `--max_cpus` or `--max_memory`).

`custom.config`
```
process {
    resourceLimits = [
        cpus: 8,
        memory: 14.GB
    ]
}
```
```bash
nextflow run doh-jdj0303/BigBacter \
    -r v2.0 \
    -c custom.config \
    -profile docker \
    --input samplesheet.csv \
    --outdir results
```

---

## Resuming a run
Nextflow can resume a run. This comes in handy when a workflow fails or when you need to make small parameter adjustments. Below is an example of how you can resume a workflow run:
```bash
nextflow run doh-jdj0303/BigBacter \
    -r v2.0 \
    -profile docker \
    --input samplesheet.csv \
    --outdir results \
    -resume
```

# Testing BigBacter
Verify that BigBacter is running properly using the command below. Update `-profile` to your preferred container engine.
```bash
nextflow run doh-jdj0303/BigBacter \
    -r v2.0 \
    -profile (docker|podman|apptainer|singularity),test \
    --outdir BigBacter_test
```
You can learn more about how the test configuration [here](https://github.com/DOH-JDJ0303/BigBacter/blob/main/conf/test.config)

# Basic Usage
In-depth overviews of [inputs](../inputs) and [outputs](../outputs/) are available. All other questions / issues should be submitted via the BigBacter [GitHub issues](https://github.com/DOH-JDJ0303/BigBacter/issues) page or by [email](mailto:waphl-bioinformatics@doh.wa.gov).