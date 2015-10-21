# what's this?

This directory contains codes to utilize data with machine learning metrics

# setting up

## make virtual environment with conda

So, I recommend to create new environment and install them with pip.

You can create virtual conda environment with
(This command takes much time)

```
conda create -n chainer python=2.7 anaconda
```

## activate virtual environment with conda

And activate virtual environment.

IMPORTANAT: Don't use `source activate [virtual env name]`. This exists shell in force if you're using pyenv.

Write pull-path to virtual environment.

You can check path to virtual environment with `conda info -e`

and activate with

```
source /home/kensuke_mitsuzawa/.pyenv/versions/anaconda-2.1.0/envs/chainer/bin/activate chainer
```

## install dependency libraries with pip 

Some packages is not able to install with conda.

you can install dependency libs. with pip 

```
[sudo] pip install -r requirement.txt
```

## installing Pylearn2

It's impossible to install PyLearn2 with package management system.

I put simple bash script which install pylearn2 and run demo code.

To execute this file, move into `using_pylearn2` directory and execute `setup_procedure.sh`


# Directory structure


    ├── README.md: this file
    ├── deep_learning: codes to call and use deep learning techniques
    ├── dimension_reduction: codes to make data into small dimension
    ├── misc: meaningless scripts
    ├── requirement.txt: pip requirement file
    ├── test: test script of python unittest
    └── using_pylearn2: simple procedure to use pylearn2 turtorial