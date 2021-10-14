import dadi
import pytest
import numpy as np
import subprocess
import glob
import os

try:
    if not os.path.exists("test_results"):
        os.makedirs("test_results")
except:
    pass

def test_InferDFE(capsys):
    threads = 3
    fits_fid = "./tests/example_data/example.two_epoch.demo.params.InferDM.bestfits"
    subprocess.run(
        "dadi-cli InferDFE " + 
        "--fs ./tests/example_data/two_epoch_non.fs --cache1d ./tests/example_data/cache_two_epoch_1d.bpkl " +
        "--demo-popt " + fits_fid + " --pdf1d lognormal --ratio 2.31 " +
        "--p0 1 1 --ubounds 10 10 --lbounds 10e-3 10e-3 " + 
        "--output-prefix ./tests/test_results/simulation.two_epoch.dfe.params --optimizations " + str(threads), shell=True
    )
    fits = glob.glob("./tests/test_results/simulation.two_epoch.dfe.params.InferDFE.opts.*")
    number_of_fits = sum([ele.startswith('#') != True for ele in open(fits[-1]).readlines()])
    assert threads == number_of_fits

#@pytest.mark.skip(reason="no way of currently testing this")
def test_InferDFE_wq(capsys):
    threads = 3
    fits_fid = "./tests/example_data/example.two_epoch.demo.params.InferDM.bestfits"
    factory = subprocess.Popen(
        "work_queue_factory -T local -M test-dfe-two-epoch -P ./tests/mypwfile --workers-per-cycle=0 --cores=1  -w " + str(threads), 
        shell=True, preexec_fn=os.setsid
        )
    subprocess.run(
        "dadi-cli InferDFE " + 
        "--fs ./tests/example_data/two_epoch_non.fs --cache1d ./tests/example_data/cache_two_epoch_1d.bpkl " +
        "--demo-popt " + fits_fid + " --pdf1d lognormal --ratio 2.31 " +
        "--p0 1 1 --ubounds 10 10 --lbounds 10e-3 10e-3 " + 
        "--output-prefix ./tests/test_results/simulation.two_epoch.dfe.params --optimizations " + str(threads) + ' ' +
        "--work-queue test-dfe-two-epoch ./tests/mypwfile", shell=True
    )
    factory.kill()
    fits = glob.glob("./tests/test_results/simulation.two_epoch.dfe.params.wq.InferDM.opts.*")
    number_of_fits = sum([ele.startswith('#') != True for ele in open(fits[-1]).readlines()])
    assert threads == number_of_fits




