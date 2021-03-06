import os
import numpy as np
from loadPreProc import NUM_CLASSES, FOR_LMAP

def rec_label(tp, fn):
	if (tp + fn) == 0:
		return -np.inf
	return tp/float(tp + fn)

def prec_label(tp, fp):
	if (tp + fp) == 0:
		return -np.inf
	return tp/float(tp + fp)

def f_label(tp, fp, fn):
	if (2*tp + fn + fp) == 0:
		return -np.inf
	return (2*tp)/float(2*tp + fn + fp)

def components_F(pred, act):
	TP = np.zeros(NUM_CLASSES)
	FP = np.zeros(NUM_CLASSES)
	FN = np.zeros(NUM_CLASSES)
	for l_id in range(NUM_CLASSES):
		for pr, ac in zip(pred, act):
			if l_id in ac:
				if l_id in pr:
					TP[l_id] += 1
				else:
					FN[l_id] += 1
			else:
				if l_id in pr:
					FP[l_id] += 1
	return TP, FP, FN			

def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(list2))
    union = (len(list1) + len(list2)) - intersection
    if union == 0:
    	return 1
    return float(intersection) / union

def set_diff(list1, list2):
    intersection = len(set(list1).intersection(list2))
    return (len(list1) + len(list2)) - (2*intersection)

def hamming_loss(pred, act):
	cnt = 0.0
	for pr, ac in zip(pred, act):
		cnt += set_diff(pr, ac)
	return cnt/(len(pred)*NUM_CLASSES)		

def write_results(metr_dict, f_res):
	print("f1 Instance: %.3f, std: %.3f" % (metr_dict['avg_fi'], metr_dict['std_fi']))
	print("f1 Lable Macro: %.3f, std: %.3f" % (metr_dict['avg_fl_ma'], metr_dict['std_fl_ma']))
	print("Jaccard Index: %.3f" % metr_dict['avg_ji'])
	print("f1 Lable Micro: %.3f" % metr_dict['avg_fl_mi'])
	print("Exact Match: %.3f" % metr_dict['avg_em'])
	print("Inverse Hamming Loss: %.3f" % metr_dict['avg_ihl'])
	f_res.write("f1 Instance: %.3f, std: %.3f\n" % (metr_dict['avg_fi'], metr_dict['std_fi']))
	f_res.write("f1 Lable Macro: %.3f, std: %.3f\n" % (metr_dict['avg_fl_ma'], metr_dict['std_fl_ma']))
	f_res.write("Jaccard Index: %.3f\n" % metr_dict['avg_ji'])
	f_res.write("f1 Lable Micro: %.3f\n" % metr_dict['avg_fl_mi'])
	f_res.write("Exact Match: %.3f\n" % metr_dict['avg_em'])
	f_res.write("Inverse Hamming Loss: %.3f\n" % metr_dict['avg_ihl'])

def insights_results(pred_vals, true_vals, posts, sen_posts, train_labels, dyn_fname_part, out_fold):
	inst_fold_str = ("%sinst/" % (out_fold))
	os.makedirs(inst_fold_str, exist_ok=True)
	dyn_fname_inst = ("%s%s.txt" % (inst_fold_str, dyn_fname_part))
	f_err_inst = open(dyn_fname_inst, 'w')
	f_err_inst.write("post\t# sents\t# words\t# words/sen\tpred cats\tactu cats\tJaccard\n")
	for pr, ac, post, sen_post in zip(pred_vals, true_vals, posts, sen_posts):
		js = jaccard_similarity(pr, ac)
		post_reco = "._ ".join(sen_post)
		num_words = len(post.split(" "))
		num_words_sen = float(num_words)/len(sen_post)
		pr_str = str(pr)[:-1][1:]
		ac_str = str(ac)[:-1][1:]
		f_err_inst.write("%s\t%d\t%d\t%.2f\t%s\t%s\t%.3f\n" % (post, len(sen_post), num_words, num_words_sen, pr_str, ac_str, js))
	f_err_inst.close()

def insights_results_lab(pred_vals, true_vals, train_labels, dyn_fname_part, out_fold,num_runs):
	train_coverage = np.zeros(NUM_CLASSES)
	for lset in train_labels:
		for l in lset:
			train_coverage[l] += 1.0
	train_coverage /= float(len(train_labels))

	dyn_fname_lab = ("%slab/%s.txt" % (out_fold, dyn_fname_part))
	f_err_lab = open(dyn_fname_lab, 'w')
	f_err_lab.write("lab id\tlabel\ttrain cov\tPrec\tRecall\tF score\n")
	class_acc ={}
	for key in range(NUM_CLASSES):
		class_acc[key] = []
	for i in range(num_runs):
		class_ind = 0
		TP, FP, FN = components_F(pred_vals[i], true_vals[i])
		for tp, fp, fn in zip(TP,FP,FN):
			P = prec_label(tp, fp)
			R = rec_label(tp, fn)
			F  = f_label(tp, fp, fn)
			class_acc[class_ind].append([P,R,F])
			class_ind += 1
	for num in range(len(class_acc)):
		mean_runs = np.mean(class_acc[num], axis = 0)
		f_err_lab.write("%d\t%s\t%.2f\t%.3f\t%.3f\t%.3f\n" % (num, FOR_LMAP[num],train_coverage[num]*100,mean_runs [0],mean_runs [1],mean_runs [2]))
	f_err_lab.close()

def aggregate_metr(metr_dict, num_vals):
	for key in ['em', 'ji', 'ihl', 'pi', 'ri', 'fi', 'pl_mi', 'rl_mi', 'fl_mi', 'pl_ma', 'rl_ma', 'fl_ma']:
		s = 0
		s_sq = 0
		for v in metr_dict[key]:
			s += v
			s_sq += v**2
		avg_v = s/num_vals
		metr_dict['avg_' + key] = avg_v
		metr_dict['std_' + key] = np.sqrt(s_sq/num_vals - avg_v**2)
		metr_dict[key] = []
	return metr_dict

def init_metr_dict():
	metr_dict = {}
	for key in ['em', 'ji', 'ihl', 'pi', 'ri', 'fi', 'pl_mi', 'rl_mi', 'fl_mi', 'pl_ma', 'rl_ma', 'fl_ma']:
		metr_dict[key] = []
	return metr_dict

def calc_metrics_print(pred_vals, true_vals, metr_dict):
	metr_dict['em'].append(exact_match(pred_vals, true_vals))
	metr_dict['ji'].append(jaccard_index_avg(pred_vals, true_vals))
	metr_dict['ihl'].append(inverse_hamming_loss(pred_vals, true_vals))
	pi, ri, fi = F_metrics_instance(pred_vals, true_vals)
	metr_dict['pi'].append(pi)
	metr_dict['ri'].append(ri)
	metr_dict['fi'].append(fi)
	TP, FP, FN = components_F(pred_vals, true_vals)
	pl_mi, rl_mi, fl_mi = F_metrics_label_micro_from_comp(TP, FP, FN)
	metr_dict['pl_mi'].append(pl_mi)
	metr_dict['rl_mi'].append(rl_mi)
	metr_dict['fl_mi'].append(fl_mi)
	pl_ma, rl_ma, fl_ma = F_metrics_label_macro_from_comp(TP, FP, FN)
	metr_dict['pl_ma'].append(pl_ma)
	metr_dict['rl_ma'].append(rl_ma)
	metr_dict['fl_ma'].append(fl_ma)
	
	return metr_dict

def exact_match(pred, act):
	cnt = 0.0
	for pr, ac in zip(pred, act):
		if set(pr) == set(ac):
			cnt += 1
	return cnt/len(pred)		

# also known as 'accuracy'
def jaccard_index_avg(pred, act):
	cnt = 0.0
	for pr, ac in zip(pred, act):
		cnt += jaccard_similarity(pr, ac)
	return cnt/len(pred)		

def inverse_hamming_loss(pred, act):
	cnt = 0.0
	for pr, ac in zip(pred, act):
		cnt += set_diff(pr, ac)
	return ((len(pred)*NUM_CLASSES)-cnt)/(len(pred)*NUM_CLASSES)

def F_metrics_instance(pred, act):
	prec = 0.0
	rec = 0.0
	for pr, ac in zip(pred, act):
		intersection = float(len(set(pr).intersection(ac)))
		prec += intersection/len(pr)
		rec += intersection/len(ac)
	prec = prec/len(pred)
	rec = rec/len(pred)
	if (prec+rec) == 0:
		f_sc = 0.0
	else:	
		f_sc = 2*prec*rec/(prec+rec) 
	return prec, rec, f_sc	

def F_metrics_label_macro(pred, act):
	TP, FP, FN = components_F(pred, act)
	return F_metrics_label_macro_from_comp(TP, FP, FN)

def F_metrics_label_macro_from_comp(TP, FP, FN):
	avgF = 0.0
	avgP = 0.0
	avgR = 0.0
	for tp, fp, fn in zip(TP,FP,FN):
		avgP += prec_label(tp, fp)
		avgR += rec_label(tp, fn)
		avgF += f_label(tp, fp, fn)

	return avgP/NUM_CLASSES, avgR/NUM_CLASSES, avgF/NUM_CLASSES

def F_metrics_label_micro(pred, act):
	TP, FP, FN = components_F(pred, act)
	return F_metrics_label_micro_from_comp(TP, FP, FN)

def F_metrics_label_micro_from_comp(TP, FP, FN):
	avgTP = np.mean(TP)
	avgFP = np.mean(FP)
	avgFN = np.mean(FN)
	return prec_label(avgTP, avgFP), rec_label(avgTP, avgFN), f_label(avgTP, avgFP, avgFN)
