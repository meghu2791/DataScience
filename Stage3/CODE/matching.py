import py_entitymatching as em

path_A = "../DATA/TableA.csv"
path_B = "../DATA/TableB.csv"

A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')
G = em.read_csv_metadata("../DATA/Labelled Set G.csv", key="_id", fk_ltable="ltable_ID", fk_rtable="rtable_ID", ltable=A, rtable=B)

# Split G into I an J
IJ = em.split_train_test(G, train_proportion=0.66, random_state=29)
I = IJ['train']
J = IJ['test']

atypes1 = em.get_attr_types(A)
atypes2 = em.get_attr_types(B)

block_c = em.get_attr_corres(A, B)
block_c['corres'] = [('title', 'title'), ('author', 'author')]

tok = em.get_tokenizers_for_blocking()
sim = em.get_sim_funs_for_blocking()

feature_table = em.get_features(A, B, atypes1, atypes2, block_c, tok, sim)

# Convert the I into a set of feature vectors using F
H = em.extract_feature_vecs(I, feature_table=feature_table, attrs_after='label',show_progress=False)
# Impute feature vectors with the mean of the column values.
H = em.impute_table(H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], strategy='mean')

# Create a set of ML-matchers
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0, probability=True)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='Naive Bayes')

# Select the best ML matcher using CV
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], k=5, target_attr='label', metric_to_select_matcher='f1', random_state=0, n_jobs=1)
print("CV stats")
print(result['cv_stats'])

# Convert the J into a set of feature vectors using F
L = em.extract_feature_vecs(J, feature_table=feature_table, attrs_after='label',show_progress=False)
L = em.impute_table(H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], strategy='mean')

#Fitting
dt.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')
svm.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')
lg.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')
ln.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')
rf.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')
nb.fit(table=H, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')

predictionsDT = dt.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')
predictionsRF = rf.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')
predictionsSVM = svm.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')
predictionsLinReg = ln.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')
predictionsLogReg = lg.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')
predictionsNB = nb.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], append=True, target_attr='predicted', inplace=False, return_probs=True, probs_attr='proba')

# Evaluate the predictions
eval_resultDT = em.eval_matches(predictionsDT, 'label', 'predicted')
print("DT")
print(em.print_eval_summary(eval_resultDT))
print()

eval_resultRF = em.eval_matches(predictionsRF, 'label', 'predicted')
print("RF")
print(em.print_eval_summary(eval_resultRF))
print()

eval_resultSVM = em.eval_matches(predictionsSVM, 'label', 'predicted')
print("SVM")
print(em.print_eval_summary(eval_resultSVM))
print()

eval_resultLinReg = em.eval_matches(predictionsLinReg, 'label', 'predicted')
print("Linear Reg")
print(em.print_eval_summary(eval_resultLinReg))
print()

eval_resultLogReg = em.eval_matches(predictionsLogReg, 'label', 'predicted')
print("Log Reg")
print(em.print_eval_summary(eval_resultLogReg))
print()

eval_resultNB = em.eval_matches(predictionsNB, 'label', 'predicted')
print("NB")
print(em.print_eval_summary(eval_resultNB))