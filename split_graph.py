

def main():
    f = open('../../evaluation/ruen.graph')
    line = f.readline()
    current_sentence_id = ''
    out = None
    while line != '':
        sentence_id = line.split(' ')[0]
        if sentence_id != current_sentence_id:
            out = open('../../evaluation/graph-parts/s' + sentence_id + '.graph', 'w')
            current_sentence_id = sentence_id
            pass

        out.write(line)

        line = f.readline()

    f.close()

    pass


main()
