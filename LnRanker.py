import math
import sys
import time

import metapy
import pytoml
import math
# from scipy import stats

class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        normalized_term_frequency = sd.doc_term_count * math.log((1+(sd.avg_dl/sd.doc_size)), 2)
        # print("{}".format(normalized_term_frequency))
        # old_score = (self.param + sd.doc_term_count) / (self.param * sd.doc_unique_terms + sd.doc_size)
        # print("{}".format(old_score))
        score = sd.query_term_weight * (normalized_term_frequency / (normalized_term_frequency + self.param)) * math.log(((sd.num_docs + 1) / (sd.corpus_term_count + 0.5)), 2)
        # print("{}".format(score))
        return score

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate, e.g. return InL2Ranker(some_param=1.0)
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index. You can ignore this for MP2.
    """
    return InL2Ranker(some_param=10.0)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    # # Examine number of documents
    # print("number of docs: {}".format(idx.num_docs()))
    # # Number of unique terms in the dataset
    # print("number of unique terms: {}".format(idx.unique_terms()))
    # # The average document length
    # print("avg document length: {}".format(idx.avg_doc_length()))
    # # The total number of terms
    # print("total corpus terms: {}".format(idx.total_corpus_terms()))

    inl2_results = []
    dirichletprior_results = []
    dirichlet_ranker = metapy.index.DirichletPrior(10)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)
    # dirichev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)


    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            # dirichlet_result = dirichlet_ranker.score(idx, query, top_k)
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
            # avg_dirich_p = dirichev.avg_p(dirichlet_result, query_start + query_num, top_k)
            inl2_results.append(avg_p)
            # dirichletprior_results.append(avg_dirich_p)
            # print("Query {} average precision: {}".format(query_num + 1, avg_p))
    # print(inl2_results)
    # print(dirichletprior_results)
    print("inl2 mean average precision: {}".format(ev.map()))
    # print("dirich mean average precision: {}".format(dirichev.map()))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
    # t_test_p_value = stats.ttest_rel(inl2_results, dirichletprior_results).pvalue
    # print("T-Test result P value: {}".format(t_test_p_value))
    # f = open("significance.txt", "w")
    # f.write(format(t_test_p_value))
    # f.close()
