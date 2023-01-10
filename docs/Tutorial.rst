Tutorial for ancIBD
======================

This page walks you through an example of using ``ancIBD`` to call IBD segments. In general, there are two mandatory steps. First, you need to transform the imputed vcf file to the so-called HDF5 file format. Second, you run ``ancIBD`` on the HDF5 file. Additionally, you can utilize the plotting function bundled within ``ancIBD`` to visualize inferred IBD segments.

Preparing Input (VCF -> HDF5)
********************************

Importantly, the input VCF file should have the following two fields, which are the key ingredients of ``ancIBD``.

* GT: Diploid Genotype (the most likely imputed diploid genotype)
* GP: Genotype probabilities for each of the three possible diploid genotypes

You can then use the function :meth:`ancIBD.IO.prepare_h5 import vcf_to_1240K_hdf` make the input format transformation.


Running the IBD Model
************************



Visualizing Inferred IBD
**************************
