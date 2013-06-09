
import sqlite3


def main():
    f = open('4.graph')
    lines = f.readlines()

    hyps = process_lines(lines)
    f.close()

    save_to_db(hyps)
    pass


def process_lines(lines):
    hyps = []
    for line in lines:
        hyps.append(parse(line))

    return hyps


def parse(line):

    line_arr = line.split(' ')
    # '4 hyp=87 stack=1 back=0 score=-1.216 transition=-1.216 forward=751 fscore=-11.551 covered=0-0 out=as one'

    hyp = {}

    for record in line_arr:
        record_arr = record.split('=')
        if len(record_arr) < 2:
            continue

        key = record_arr[0]
        value = record_arr[1]
        if key != 'out':
            hyp[key] = value
        else:
            cut_from = line.rfind('=') + 1
            cut_to = len(line) - 1
            hyp['out'] = line[cut_from:cut_to]

    if hyp['hyp'] == '0':
        init_first_hyp(hyp)

    if not 'recombined' in hyp:
        hyp['recombined'] = '-1'

    return hyp


def init_first_hyp(hyp):
    hyp['back'] = '-1'
    hyp['score'] = '-1'
    hyp['transition'] = '-1'
    hyp['recombined'] = '-1'
    hyp['forward'] = '-1'
    hyp['fscore'] = '-1'
    hyp['covered'] = '-1'
    hyp['out'] = '-1'


def save_to_db(hyps):
    conn = sqlite3.connect('graph.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE hypotheses
             (hyp, stack, back, score, transition, recombined, forward, fscore, covered, out)''')

    for hyp in hyps:
        c.execute('''INSERT INTO hypotheses VALUES (%(hyp)s, %(stack)s, %(back)s, %(score)s, %(transition)s,
                  %(recombined)s, %(forward)s, %(fscore)s, '%(covered)s', '%(out)s')''' % hyp)

    conn.commit()
    conn.close()

main()
