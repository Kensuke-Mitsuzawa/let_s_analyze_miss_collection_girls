# Your shell settingfile
YOUR_SHELL_SETTINGS=~/.bashrc
YOUR_SHELL_COMMAND_TO_SHOW_PNG="open -Wn"
pylearn2_using_top_dir=`pwd`

# -------------------------------------------------------
# set environment variables
git clone git://github.com/lisa-lab/pylearn2.git
cd pylearn2
python setup.py build
sudo python setup.py install
cd ../
# -------------------------------------------------------
# download test-data
mkdir pylearn2_data
cd ./pylearn2_data
mkdir mnist
cd mnist
wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
for f in `ls`; gzip -dv $f

cd ../
mkdir cifar10
cd cifar10
wget http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
gzip -dv cifar-10-python.tar.gz
tar -xvf cifar-10-python.tar

# -------------------------------------------------------
# set setting path
echo "" >> ${YOUR_SHELL_SETTINGS}
echo "# These settings are for pylearn2" >> ${YOUR_SHELL_SETTINGS}
echo "export PYLEARN2_DATA_PATH=`pwd`/pylearn2_data" >> ${YOUR_SHELL_SETTINGS}
echo 'export PYLEARN2_VIEWER_COMMAND="${YOUR_SHELL_COMMAND_TO_SHOW_PNG}"' >> ${YOUR_SHELL_SETTINGS}
echo "export PATH=`pwd`/pylearn2/pylearn2/scripts:\$PATH" >> ${YOUR_SHELL_SETTINGS}
# -------------------------------------------------------
# run test script
cd ${pylearn2_using_top_dir}pylearn2/pylearn2/scripts/tutorials/grbm_smd
python make_dataset.py
train.py cifar_grbm_smd.yaml
show_weights.py --out=weights.png cifar_grbm_smd.pkl
print_monitor.py cifar_grbm_smd.pkl