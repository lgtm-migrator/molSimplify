from argparse import Namespace
from molSimplify.Scripts.jobgen import sgejobgen, slurmjobgen


def test_sgejobgen_default(tmpdir):
    args = Namespace(jname=None, jid=1, wtime=None, memory=None,
                     queue=None, qccode=None, cpus=None, gpus=None,
                     joption=None, modules=None, jcommand=None)
    sgejobgen(args, [str(tmpdir)])
    with open(tmpdir / 'jobscript') as fin:
        lines = fin.read()
    lines_ref = ('#$ -S /bin/bash\n'
                 '#$ -N job1\n'
                 '#$ -R y\n'
                 '#$ -cwd\n'
                 '#$ -l h_rt=168:00:00\n'
                 '#$ -l h_rss=8G\n'
                 '#$ -q cpus\n'
                 '#$ -l cpus=1\n'
                 '#$ -pe smp 1\n'
                 'export OMP_NUM_THREADS=1\n')
    assert lines == lines_ref


def test_sgejobgen(tmpdir):
    args = Namespace(jname='test', jid=1, wtime='90', memory='4G',
                     queue='gpusbig', qccode='terachem', cpus=None, gpus='2',
                     joption=None, modules=['openmp'], jcommand=None)
    sgejobgen(args, [str(tmpdir)])
    with open(tmpdir / 'jobscript') as fin:
        lines = fin.read()
    lines_ref = ('#$ -S /bin/bash\n'
                 '#$ -N test1\n'
                 '#$ -R y\n'
                 '#$ -cwd\n'
                 '#$ -l h_rt=90:00:00\n'
                 '#$ -l h_rss=4G\n'
                 '#$ -q gpusbig\n'
                 '#$ -l gpus=2\n'
                 '#$ -pe smp 2\n'
                 'module load openmp\n'
                 'export OMP_NUM_THREADS=2\n'
                 'terachem terachem_input > $SGE_O_WORKDIR/opttest.out\n\n'
                 'sleep 30')
    assert lines == lines_ref


def test_slurmjobgen_default(tmpdir):
    args = Namespace(jname=None, jid=1, wtime=None, memory=None,
                     queue=None, qccode=None, joption=None, modules=None,
                     jcommand=None)
    slurmjobgen(args, [str(tmpdir)])
    with open(tmpdir / 'jobscript') as fin:
        lines = fin.read()
    lines_ref = ('#!/bin/bash\n'
                 '#SBATCH --job-name=job1\n'
                 '#SBATCH --output=batch.log\n'
                 '#SBATCH --export=ALL\n'
                 '#SBATCH -t 168:00:00\n'
                 '#SBATCH --mem==8G\n'
                 '#SBATCH --partition=cpus\n'
                 '#SBATCH --nodes=1\n'
                 '#SBATCH --ntasks-per-node=1\n')
    assert lines == lines_ref


def test_slurmjobgen(tmpdir):
    args = Namespace(jname='test', jid=1, wtime='90', memory='4G',
                     queue='testqueue', qccode='qchem', joption=None,
                     modules=None, jcommand=None)
    slurmjobgen(args, [str(tmpdir)])
    with open(tmpdir / 'jobscript') as fin:
        lines = fin.read()
    lines_ref = ('#!/bin/bash\n'
                 '#SBATCH --job-name=test1\n'
                 '#SBATCH --output=batch.log\n'
                 '#SBATCH --export=ALL\n'
                 '#SBATCH -t 90:00:00\n'
                 '#SBATCH --mem=4G\n'
                 '#SBATCH --partition=testqueue\n'
                 '#SBATCH --nodes=1\n'
                 '#SBATCH --ntasks-per-node=1\n'
                 'qchem qch.inp 1 > qch.out')
    assert lines == lines_ref
