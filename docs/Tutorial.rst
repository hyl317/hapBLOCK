Tutorial for ancIBD
======================

This page walks you through an example of using ``ancIBD`` to call IBD segments. In general, there are two mandatory steps. First, you need to transform the imputed vcf file to the so-called HDF5 file format. Second, you run ``ancIBD`` on the HDF5 file. Additionally, you can utilize the plotting function bundled within ``ancIBD`` to visualize inferred IBD segments. This visual test is always recommended to verify whether your data is sound and everything works as expected.

Preparing Input (VCF -> HDF5)
********************************

Importantly, the input VCF file should have the following two fields, which are the key ingredients of ``ancIBD``.

* GT: Diploid Genotype (the most likely imputed diploid genotype)
* GP: Genotype probabilities for each of the three possible diploid genotypes

You can then use the function :meth:`ancIBD.IO.prepare_h5.vcf_to_1240K_hdf` make the input format transformation. 

Below you will find the function call for a single chromosome (please replace the hard-coded path with your own). You can write a loop, or also use an array job to run this function on a cluster and parallelize over all chromosomes.
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

With the HDF5 file for each autosome at hand, we can now call IBD segments on them. We will use the function :meth:`ancIBD.run.hapBLOCK_chroms`.
In the following samples we run ``ancIBD`` on six samples from the Hazelton data.

.. code-block:: python

    from ancIBD.run import hapBLOCK_chroms
    iids = ["I12439", "I12440", "I12438", 
        "I12896", "I21390", "I30300"] # The six Hazelton Indivdiuals of the example data.
    for ch in range(1,23):
        df_ibd = hapBLOCK_chroms(folder_in='./data/hdf5/example_hazelton_chr',
                             iids=iids, run_iids=[],
                             ch=ch, folder_out='./output/ibd_hazelton/',
                             output=False, prefix_out='', logfile=False,
                             l_model='hdf5', e_model='haploid_gl', h_model='FiveStateScaled', t_model='standard',
                             ibd_in=1, ibd_out=10, ibd_jump=400,
                             min_cm=6, cutoff_post=0.99, max_gap=0.0075,
                             processes=1)

The function :meth:`ancIBD.run.hapBLOCK_chroms` calls IBD of an input hdf5. It outputs a dataframe of IBD, which below the function is saved into a specified output folder.

Important parameters varying from application to application are:

* folder_in: The path of the hdf5 files used for IBD calling. The format is so that everything up to the chrosome number is specified.
* iids: All iids to load from the hdf. Has to match the IIDs in the sample field of the HDF5
* run_iids: Which pairs to run [[iid1, iid2], ...] If this parameter is left empty, then all pairwise samples from the list iids are run.

The other parameters specifiying the various modes of ancIBD, and the parameters are default values. E.g. ibd_in, ibd_out, ibd_jump control the jump rates of the underlying HMM (in rates per Morgan), and the various _model parameter specificy the type of input data. Power users can modify those settings, but the default values are the recommend parameters for default human data.

At the end we combine results across all autosomes. 

.. code-block:: python

    from ancIBD.IO.ind_ibd import combine_all_chroms
    combine_all_chroms(chs=range(1,23),
                   folder_base='./output/ibd_hazelton/ch',
                   path_save='./output/ibd_hazelton/ch_all.tsv')


Aside from the raw IBD segment calls, you can also obtain a summary table showing the number and total sum of IBD in various length bins. This could be helpful for quickly identifying relatives.
The function :meth:`ancIBD.IO.ind_ibd.create_ind_ibd_df` outputs a summary table (pandas dataframe). Each row is one pair of individuals, and there are columns for summary statistics:

* max_ibd: Maximum Length of IBD
* sum_IBD>x: The total length of all IBD segments longer than x Morgan
* n_IBD>x: The total number of all IBD segments longer than x Morgan

By default, these are recorded for >8,>12,>16 and >20 Morgan. This can be changed with the min_cms keyword.
The function also does post-processing of trustworthy IBD blocks. Most importantly, only IBD with at least a certain SNP density are kept (the default is to have at least 220 SNPs per cM). The reason for this is that areas of low SNP density (such as regions with large gaps of SNPs) are very prone to false positives. 

.. code-block:: python

    from ancIBD.IO.ind_ibd import create_ind_ibd_df
    df_res = create_ind_ibd_df(ibd_data = './output/ibd_hazelton/ch_all.tsv',
                      min_cms = [8, 12, 16, 20], snp_cm = 220, min_cm = 5, sort_col = 0,
                      savepath = "./output/ibd_hazelton/ibd_ind.d220.tsv")


Visualizing Inferred IBD
**************************
