import os, time, inspect
from dadi_cli.Models import get_model
from dadi_cli.Pdfs import get_dadi_pdf
from dadi_cli.Pdfs import get_dadi_pdf_params
from dadi_cli.utilities import pts_l_func
import dadi


def simulate_demography(
    model, model_file, p0, ns, pts_l, misid, output, inference_file
):
    if pts_l == None:
        pts_l = (int(ns * 1.1) + 2, int(ns * 1.2) + 4, int(ns * 1.3) + 6)
    # fs = dadi.Numerics.make_extrap_func(get_dadi_model_func(model, model_file))(popt, fs.sample_sizes, pts_l)*theta
    func, params = get_model(model, model_file)
    if misid:
        param_names = func.__param_names__
        func = dadi.Numerics.make_anc_state_misid_func(func)
        func.__param_names__ = param_names + ["misid"]
    func_ex = dadi.Numerics.make_extrap_func(func)
    fs = func_ex(p0, ns, pts_l)
    fs.to_file(output)
    if inference_file:
        fi = open(output + ".SimulateDM.pseudofit", "w")
        fi.write(
            "# Ran SimulateDM\n# This is a fake inference output results to generate caches\n# Log(likelihood)   "
            + "\t".join(func.__param_names__)
            + "\ttheta0\n"
            "-0\t" + "\t".join([str(ele) for ele in p0]) + "\t1"
        )
        fi.close()


def simulate_demes(demes_file, ns, pts_l, pop_ids, output):
    if pts_l == None:
        pts_l = (int(ns * 1.1) + 2, int(ns * 1.2) + 4, int(ns * 1.3) + 6)
    fs = dadi.Spectrum.from_demes(
        demes_file, sampled_demes=pop_ids, sample_sizes=ns, pts=pts_l
    )
    fs.to_file(output)


def simulate_dfe(p0, cache1d, cache2d, sele_dist, sele_dist2, ratio, misid, output):

    if cache1d != None:
        func = cache1d.integrate
    if cache2d != None:
        func = cache2d.integrate

    if sele_dist != None:
        sele_dist = get_dadi_pdf(sele_dist)
    if sele_dist2 != None:
        sele_dist2 = get_dadi_pdf(sele_dist2)
    if (sele_dist == None) and (sele_dist2 != None):
        sele_dist = sele_dist2

    if (cache1d != None) and (cache2d != None):
        func = dadi.DFE.Cache2D_mod.mixture
        func_args = [cache1d, cache2d, sele_dist, sele_dist2, ratio]
    else:
        func_args = [sele_dist, ratio]

    if misid:
        func = dadi.Numerics.make_anc_state_misid_func(func)
    print(p0, None, sele_dist, ratio, None)
    # Get expected SFS for MLE
    if (cache1d != None) and (cache2d != None):
        fs = func(p0, None, cache1d, cache2d, sele_dist, sele_dist2, ratio, None)
    else:
        fs = func(p0, None, sele_dist, ratio, None)
    fs.to_file(output)