
import sqlite3

def rephrase(output_sentence, input, db, n_results):
    phrases = parse_phrases(output_sentence)
    intervals = find_involved_intervals(input, phrases)
    paraphrases = get_paraphrases(intervals, db, n_results)

    return paraphrases


def parse_phrases(mt_out):

    phrases = []
    mt_out_arr = mt_out.split('|')
    mt_out_arr_len = len(mt_out_arr)
    i = 0
    tail = -1

    while i < mt_out_arr_len - 1:
        head = tail + 1
        tail = head + len(mt_out_arr[i]) - 1

        phrases.append({
            'content': mt_out_arr[i],
            'coverage': mt_out_arr[i + 1],
            'head': head,
            'tail': tail
        })

        i += 2

    return phrases


def find_involved_intervals(input, phrases):

    intervals = []

    mt_out = u''
    for phrase in phrases:
        mt_out += phrase['content']

    left = mt_out.index(u'' + input)
    right = left + len(input)

    for phrase in phrases:
        head = int(phrase['head'])
        tail = int(phrase['tail'])
        if (head <= right) and (tail >= left):
            intervals.append(phrase['coverage'])

    return intervals


def get_paraphrases(intervals, db, n_results):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    partials = []

    for interval in intervals:
        hypotheses = []
        c.execute("select out from hypotheses where covered = '%s' order by score desc" % interval)

        for row in c.fetchall():
            hypotheses.append(row[0])

        partials.append(hypotheses)

    conn.close()

    paraphrases = []
    for i in range(0, n_results):
        paraphrase = ''
        for j in range(0, len(partials)):
            paraphrase += partials[j][i] + ' '
        paraphrases.append(paraphrase)

    return paraphrases


