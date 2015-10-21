# What's this?

This directory has code to use deep learning technique, which learn features with non-supervised learning.

Now, this directory has 2-types of libraries.

* chainer
* pylearn2

# directory strucutre

directories

    * intermediate_files_pylearn2: directory for datasource/trained model for pylearn2 
    * model_pylearn2: yaml model definition file for pylearn2
    * graphs: directory for graph and visualized weight in chainer
    * models: model scripts files for chainer 
    * trained_models: directory for trained chainer model


scripts

    * data_loader.py: script to load picture data and make input matrix
    * draw_graphs.py: visualize learned weight(make *png file)
    * train_model.py: generic training script for chainer
    * exp_interface.py: experimental interface script of chainer
    * make_dataset_pylearn2: script to make dataset for pylearn2(datasource of pylearn2 is a little bit different from chainer)
    * show_weight_pylearn2: script to make visualized *png file for pylearn2
    * train_model_pylearn2: training script for pylearn2
