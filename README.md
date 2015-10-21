# what's this?

This project is all codes to utilize the data from Japanese Miss/Mr contest.

For now, this project contains following contents

* Extract information from Miss/Mr web site
* Automatic Face recognition
* Extract and make picture embedded into dense vector space with DeepNN
* Dimension reduction with LSI, SVD, tSNE
* Visualize 2-dimension plot with interactive scatter graph

# setting up

プロジェクトの大部分で機械学習系のライブラリを利用します。

pyenvのanaconda環境を利用すると良いでしょう。

* [ubuntuの場合のpyenv setup 参考](http://qiita.com/5t111111/items/e170fead91261621b054)
* [macの場合のpyenv setup 参考](http://hogehuga.com/post-241/)

pyenvを利用できる準備ができたら、

`[sudo] pyenv install anaconda-2.1.0`

でanaconda-2.1.0の環境を用意します。

`pyenv global anaconda-2.1.0` でanaconda環境への切り替えが可能です。
