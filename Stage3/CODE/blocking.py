import py_entitymatching as em

path_A = "../DATA/TableA.csv"
path_B = "../DATA/TableB.csv"

A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')

ob = em.OverlapBlocker()

C1= ob.block_tables(A, B, 'title', 'title', word_level=True, overlap_size=3, l_output_attrs=['title','author'], r_output_attrs=['title','author'], show_progress=False)
C2 = ob.block_candset(C1, 'author', 'author', word_level=True, overlap_size=1, show_progress=False)

qgm_3 = em.get_tokenizers_for_blocking()['qgm_3']
jaccard = em.get_sim_funs_for_blocking()['jaccard']

def bbRule(ltuple, rtuple):
    l_title = ltuple['title'].split()
    r_title = rtuple['title'].split()
    if len(l_title) < 3 and (len(r_title) == len(l_title)):
        for i in range(len(l_title)):
            if (l_title[i] != r_title[i]):
                return True
            if (jaccard(qgm_3(ltuple['author']), qgm_3(rtuple['author'])) < 0.5):
                return True
        return False
    else:
        return True

bb = em.BlackBoxBlocker()
bb.set_black_box_function(bbRule)
D = bb.block_tables(A, B, l_output_attrs=['title','author'], r_output_attrs=['title','author'])

#Union
Z = em.combine_blocker_outputs_via_union([C2, D])
#Z.to_csv(path_or_buf=csv2)

#Debugging
dbg = em.debug_blocker(Z, A, B, output_size=200)
#dbg.to_csv(path_or_buf=csv3)