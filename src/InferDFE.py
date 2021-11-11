import dadi
import dadi.DFE
#import dadi.NLopt_mod
import nlopt
import os, time
import numpy as np
from src.Pdfs import get_dadi_pdf

def infer_dfe(fs, cache1d, cache2d, sele_dist, sele_dist2, theta,
              p0, upper_bounds, lower_bounds, fixed_params, misid, cuda, maxeval, maxtime, seed):

    # Randomize starting parameter values
    if seed != None: 
        np.random.seed(seed)
    else:
        ts = time.time()
        seed = int(time.time()) + int(os.getpid())
        np.random.seed(seed)

    # fs = dadi.Spectrum.from_file(fs)

    # theta = ns_s * theta
    # #popt = np.array(open(popt, 'r').readline().rstrip().split(), dtype=float)
    # #theta = ns_s * popt[-1]

    if cache1d != None:
        # spectra1d = pickle.load(open(cache1d, 'rb'))
        func = cache1d.integrate
    if cache2d != None:
        # spectra2d = pickle.load(open(cache2d, 'rb'))
        func = cache2d.integrate
   
    if sele_dist != None: 
        sele_dist = get_dadi_pdf(sele_dist)
    if sele_dist2 != None:
        sele_dist2 = get_dadi_pdf(sele_dist2)
    if (sele_dist == None) and (sele_dist2 != None):
        sele_dist = sele_dist2
    
    if (cache1d != None) and (cache2d != None):
        func = dadi.DFE.Cache2D_mod.mixture
        func_args = [cache1d, cache2d, sele_dist, sele_dist2, theta]
    else:
        func_args = [sele_dist, theta]
        
    if misid:
        func = dadi.Numerics.make_anc_state_misid_func(func)

    # print('Inputs\n',p0,'\n',lower_bounds,'\n',upper_bounds,'\n',fixed_params,'\n\n')
    p0_len = len(p0)
    p0 = _convert_to_None(p0, p0_len)
    lower_bounds = _convert_to_None(lower_bounds, p0_len)
    upper_bounds = _convert_to_None(upper_bounds, p0_len)
    fixed_params = _convert_to_None(fixed_params, p0_len)

    # Fit a DFE to the data
    # Initial guess and bounds
    #print(p0)
    # print('Inputs\n',p0,'\n',lower_bounds,'\n',upper_bounds,'\n',fixed_params,'\n\n')
    print(func)
    p0 = dadi.Misc.perturb_params(p0, lower_bound=lower_bounds, upper_bound=upper_bounds)
    popt, _ = dadi.Inference.opt(p0, fs, func, pts=None, 
                                func_args=func_args, fixed_params=fixed_params,
                                lower_bound=lower_bounds, upper_bound=upper_bounds,
                                maxeval=maxeval, maxtime=maxtime, multinom=False, verbose=0)
    # print(popt)

    #print('Optimized parameters: {0}'.format(popt))

    # Get expected SFS for MLE
    if (cache1d != None) and (cache2d != None):
        model = func(popt, None, cache1d, cache2d, sele_dist, sele_dist2, theta, None)
    else:
        model = func(popt, None, sele_dist, theta, None)
    #print(model)
    # Likelihood of the data given the model AFS.
    ll_model = dadi.Inference.ll_multinom(model, fs)
    #print('Maximum log composite likelihood: {0}'.format(ll_model))

    #with open(output, 'w') as f:
    #    f.write(str(ll_model))
    #    for p in popt:
    #        f.write("\t")
    #        f.write(str(p))
    #    f.write("\n")
    return ll_model, popt, theta

def _convert_to_None(inference_input, p0_len):
    if inference_input == -1: inference_input = [inference_input]*p0_len
    inference_input = list(np.where(np.array(inference_input) == -1, None, np.array(inference_input)))
    return inference_input

