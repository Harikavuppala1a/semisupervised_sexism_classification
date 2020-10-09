# semisupervised_sexism_classification

This repository contains code for our paper titled "Fine-grained Multi-label Sexism Classificationusing Semi-supervised Learning" published in WISE-2020.

Abstract:
Sexism, a pervasive form of oppression, causes profound suffering through various manifestations. Given the rising number of experiences of sexism reported online, categorizing these recollections automatically can aid the fight against sexism, as it can facilitate effective analyses by gender studies researchers and government officials involved in policy making. In this paper, we explore the fine-grained, multi-label classification of accounts (reports) of sexism. To the best of our knowledge, we consider substantially more categories of sexism than any related prior work through our 23-class problem formulation. Moreover, we present the first semi-supervised work for the multi-label classification of accounts describing any type(s) of sexism wherein the approach goes beyond merely fine-tuning pre-trained models using unlabeled data. We devise self-training based techniques tailor-made for the multi-label nature of the problem to utilize unlabeled samples for augmenting the labeled set. We identify high textual diversity with respect to the existing labeled set as a desirable quality for candidate unlabeled instances and develop methods for incorporating it into our approach. We also explore ways of infusing class imbalance alleviation for multi-label classification into our semi-supervised learning, independently and in conjunction with the method involving diversity. Several proposed methods outperform a variety of baselines on a recently released dataset for multi-label sexism categorization across several standard metrics.

Instructions for using our code:
In order to generate the augment data using any of the proposed methods, run gen_augment_data.py.
Once the augmented data is generated, run main.py to generate the results.
To generate results for all the deep learning baselines and proposed methods, run main.py.
To generate results for traditional machine leanring baselines, run TraditionalML_LP.py.
For all these .py files, pass the config files mentioned in the data folder as arguments (e.g., python gen_augment_data.py data/config_deep_learning.txt).
All the hyperparameters are available in Tuned hyper-parameters.pdf file.

If you use this code for any research, please cite:

Harika Abburi, Pulkit Parikh, Niyati Chhaya and Vasudeva Varma. 2020. Fine-grained Multi-label Sexism Classificationusing Semi-supervised Learning. In Proceedings of the 21st International Conference on Web Information Systems Engineering (WISE), Amsterdam and Leiden, Netherlands

