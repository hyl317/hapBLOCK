Tutorial for ancIBD
======================

This page walks you through an example of using ``ancIBD`` to call IBD segments. In general, there are two mandatory steps. First, you need to transform the imputed vcf file to the so-called HDF5 file format. Second, you run ``ancIBD`` on the HDF5 file. Additionally, you can utilize the plotting function bundled within ``ancIBD`` to visualize inferred IBD segments.

Preparing Input (VCF -> HDF5)
********************************

Importantly, the input VCF file should have the following two fields, which are the key ingredients of ``ancIBD``.

* GT: Diploid Genotype (the most likely imputed diploid genotype)
* GP: Genotype probabilities for each of the three possible diploid genotypes

You can then use the function :meth:`ancIBD.IO.prepare_h5.vcf_to_1240K_hdf` make the input format transformation. 

Below you find the function call for a single chromosome. You can write a loop, or also use an array job to run this function on a cluster and parallelize over all chromosomes.
For large datasets, this step could take some time, so parallelization over chromosomes is recommended.

.. code-block:: python
    ch = 22
    base_path = f"/n/groups/reich/hringbauer/git/hapBLOCK"
    vcf_to_1240K_hdf(in_vcf_path = f"./data/vcf.raw/example_hazelton_chr{ch}.vcf",
                 path_vcf = f"./data/vcf.1240k/example_hazelton_chr{ch}.vcf",
                 path_h5 = f"./data/hdf5/example_hazelton_chr{ch}.h5",
                 marker_path = f"./data/filters/snps_bcftools_ch{ch}.csv",
                 map_path = f"./data/v51.1_1240k.snp", 
                 af_path = f"./data/afs/v51.1_1240k_AF_ch{ch}.tsv",
                 col_sample_af = "", 
                 buffer_size=20000, chunk_width=8, chunk_length=20000,
                 ch=ch)


Running the IBD Model
************************



Visualizing Inferred IBD
**************************
