
def filter_paraphrases(partials, n_results):
    paraphrases = []
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
