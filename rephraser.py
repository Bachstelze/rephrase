
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
        tail = head + len(mt_out_arr[i]) - 2

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

    mt_out = ''
    for phrase in phrases:
        mt_out += phrase['content'].strip() + ' '

    try:
        input = input.decode('utf-8', 'ignore').encode('windows-1252', 'backslashreplace')
        mt_out = mt_out.decode('utf-8', 'ignore').encode('windows-1252', 'backslashreplace')

        if input in mt_out:
            left = mt_out.index(input)
            right = left + len(input)

            for phrase in phrases:
                head = int(phrase['head'])
                tail = int(phrase['tail'])
                if (head < right) and (tail >= left):
                    intervals.append(phrase['coverage'])
        else:
            print 'bad alignment'
    except UnicodeEncodeError:
        print 'bad encoding'

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
        if len(partials) > 0:
            for j in range(0, len(partials)):
                if i >= len(partials[j]):
                    paraphrase = ''
                    break
                paraphrase += partials[j][i] + ' '
        if paraphrase != '':
            paraphrases.append(paraphrase)

    return paraphrases


