# semisupervised_sexism_classification

As we are making use of the best-performing model from [1] in our semi-supervised
methods, we use parts of the code from that paper
1. generating_augment_data.py
Generates augmented data for various proposed methods
2. main.py
The main file to run for all the deep learning based methods including the proposed
approach and baselines after generating the augmented data
3. arranging.py
Used to save the glove and bert features corresponding to the augmented data
4. dlModels.py
Deep learning architectures for various methods
5. evalMeasures.py
Consists of functions used for multi-label evaluations
6. loadPreProc.py
Data loading and preprocessing functions
7. TraditionalML_LP.py
Consists of various traditional machine learning methods
8. Config_traditional_ML.txt
Configuration for traditional ML methods
9. Config_deep_learning.txt
Configuration file for proposed semi-supervised methods and deep learning methods
10. gen_batch_keras.py, neuralApproaches.py, sent_enc_embed.py, word_embed.py -
Reproduced from [1]
References
1. Parikh, P., Abburi, H., Badjatiya, P., Krishnan, R., Chhaya, N., Gupta, M., Varma,
V.: Multi-label categorization of accounts of sexism using a neural framework.
arXiv preprint, arXiv:1910.04602 (2019).
