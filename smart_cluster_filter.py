
# import subprocess

def filter_paraphrases(partials, n_results, mt_out, phrases, intervals, scores):
    global PHRASES
    global MT_OUT
    global INTERVALS
    global SCORES
    MT_OUT = mt_out
    PHRASES = phrases
    INTERVALS = intervals
    SCORES = scores

    paraphrases = []
    clustered_partials = cluster_partials(partials)
    sorted_clustered_partials = sort_clusters(clustered_partials)
    partials = flatten_partials(sorted_clustered_partials)
    for i in range(0, n_results):
        paraphrase = ''
        if len(partials) > 0:
            for j in range(0, len(partials)):
                if i >= len(partials[j]):
                    paraphrase = ''
                    break
                paraphrase += partials[j][i] + ' '
        if paraphrase != '':
            paraphrases.append(paraphrase)


    return paraphrases

def cluster_partials(partials):
    stopwords = load_stopwords()
    clustered_partials = []

    for partial in partials:
        clustered_partial = {}
        for phrase in partial:
            phrase_parts = phrase.split(' ')
            cluster_key = ''
            for part in phrase_parts:
                if not (part + '\n') in stopwords:
                    cluster_key += part + ' '

            cluster_key = cluster_key.strip()
            if not cluster_key in clustered_partial:
                clustered_partial[cluster_key] = [phrase]
            elif not phrase in clustered_partial[cluster_key]:
                clustered_partial[cluster_key].append(phrase)

        clustered_partials.append(clustered_partial)
    return clustered_partials

def load_stopwords():
    f = open('stopwords.txt')
    stopwords = f.readlines()
    f.close()
    return stopwords


def cluster_score(phrase, index):
    return -SCORES[phrase]

#
#def lm_score(str):
##    lm_result = subprocess.check_output(["sh", "lm.sh", "'" + str + "'"])
##    try:
##        score = float(lm_result.split('Total: ')[1].split(' OOV:')[0])
##    except :
##        score = -9999.9
#    return -len(str)


def sort_clusters(clustered_partials):
    sorted_clustered_partials = []
    partial_index = 0
    for clustered_partial in clustered_partials:
        sorted_clustered_partial = {}
        for key in clustered_partial:
            sorted_clustered_partial[key] = sorted(clustered_partial[key], key=lambda phrase: cluster_score(phrase, partial_index))
        sorted_clustered_partials.append(sorted_clustered_partial)
        partial_index += 1
    return sorted_clustered_partials

def flatten_partials(sorted_clustered_partials):
    flat_partials = []
    for partial in sorted_clustered_partials:
        flat_partial = []
        for i in range(0, 15):
            for key in partial:
                if len(partial[key]) > i:
                    flat_partial.append(partial[key][i])

        flat_partials.append(flat_partial)
    return flat_partials