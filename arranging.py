import os
import shutil
import h5py


def get_elmo_embeddings(path_rearr_src,path_rearr_dst, index_filename,len_augmented):
	os.makedirs(path_rearr_dst, exist_ok=True)
	file_index = 0
	f_res = open(index_filename, 'r')
	for line in f_res.readlines():
		if file_index < len_augmented:
			row = line.strip()
			src = str(row) + ".npy"
			dst = str(file_index) + ".npy"
			shutil.copy(path_rearr_src + src,path_rearr_dst+dst)
			file_index = file_index + 1
		else:
			break

def get_bert_embeddings(path_rearr_src,path_rearr_dst, index_filename,data_dict):
	f_res = open(index_filename, 'r')
	indexes =[]
	file_index = 0
	for line in f_res.readlines():
		if file_index < data_dict['test_en_ind']:
			indexes.append(int(line.strip()))
			file_index = file_index + 1
		else:
			break
	with h5py.File(path_rearr_src,"r") as hf:
		bert_feat = hf['feats'][:data_dict['testunlab_en_ind']]
	bert_edited = [bert_feat[i] for i in indexes]
	with h5py.File(path_rearr_dst, "w") as hfile:
		hfile.create_dataset('feats', data=bert_edited) 
	