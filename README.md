# dadi-CLI

`dadi-CLI` provides a command line interface for [dadi](https://bitbucket.org/gutenkunstlab/dadi/src/master/) to help users to quickly apply `dadi` to their research. `dadi` is a flexible python package for inferring demographic history and the distribution of fitness effects (DFE) from population genomic data based on diffusion approximation. 

## Installation

## Usage

### Generating frequency spectrum from VCF files
### Inferring demographic models
### Generating caches for DFE inference
### Inferring DFE
### Performing statistical testing
### Plotting

`dadi-CLI` can plot frequency spectrum from data or compare the spectra between model and data.

To plot frequency spectrum from data, we use

    dadi-CLI Plot --fs example.fs --output example.fs.pdf
    
To compare two frequency spectra from data, we use

    dadi-CLI Plot --fs example1.fs --fs2 example2.fs --output example.fs.comparison.pdf
    
To compare frequency spectra between a demographic model without selection and data, we use

    dadi-CLI Plot --fs example.fs 
    
To compare frequency spectra between a demographic model with selection and data, we use

    dadi-CLI Plot --fs
    
### Available demographic models

`dadi-CLI` also provides a command `Model` to help users finding available demographic models in `dadi`.
To find out available demographic models, we use

    dadi-CLI Model --names
    
Then the available demographic models will be displayed in the screen

    Available 1D demographic models:
    - bottlegrowth_1d
    - growth_1d
    - snm_1d
    - three_epoch_1d
    - two_epoch_1d

    Available 2D demographic models:
    - bottlegrowth_2d
    - bottlegrowth_split
    - bottlegrowth_split_mig
    - IM
    - IM_pre
    - split_mig
    - split_asym_mig
    - snm_2d

    Available demographic models with selection:
    - equil
    - equil_X
    - IM_sel
    - IM_sel_single_gamma
    - IM_pre_sel
    - IM_pre_sel_single_gamma
    - split_mig_sel
    - split_mig_sel_single_gamma
    - split_asym_mig_sel
    - split_asym_mig_sel_single_gamma
    - two_epoch_sel
    - mixture

To find out the parameters and detail of a specific model, we can use the name of the demograpic model as the parameter after `--names`. For example,

    dadi-CLI Model --names IM
    
Then the detail of the model will be displayed in the screen.

    - IM:

            Isolation-with-migration model with exponential pop growth.
            Two populations in this model.

            params = [s,nu1,nu2,T,m12,m21]

                  s: Size of pop 1 after split (Pop 2 has size 1-s)
                nu1: Final size of pop 1 (in units of Na)
                nu2: Final size of pop 2 (in units of Na)
                  T: Time in the past of split (in units of 2*Na generations)
                m12: Migration from pop 2 to pop 1 (2*Na*m12)
                m21: Migration from pop 1 to pop 2 (2*Na*m21)

### Available DFE distributions

## References

[Gutenkunst et al., *PLoS Genet*, 2009.](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1000695)