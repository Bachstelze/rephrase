
import rephraser
import json

def main():

    f = open('align.out.json')
    align_data = json.load(f)
    f.close()

    f = open('en2.out')
    en2_out_lines = f.readlines()
    f.close()

    current_line = 1
    correct = 0

    START = 0
    FINISH = 1000
    N = 15

    logs = {
        'tests': [],
        'numberOfTests': FINISH - START,
        'numberOfOutputs': N
    }

    for line in en2_out_lines:
        if current_line < START:
            current_line += 1
            continue
        if current_line > FINISH:
            break
        print 'Testing sentence #' + str(current_line)
        test_pairs = align_data[str(current_line)]
        for test_pair in test_pairs:
            paraphrases = rephraser.rephrase(line, test_pair['corrupted'], '../../evaluation/graph-dbs/s' + str(current_line-1) + '.graph.db', N)
            correct_case = False
            for paraphrase in paraphrases:
                if test_pair['original'].strip() == paraphrase.strip():
                    correct += 1
                    correct_case = True
                    break
            logs['tests'].append({
                'lineNo': f_enc(current_line),
                'pair': test_pair,
                'line': f_enc(line),
                'paraphrases': paraphrases,
                'correct': correct_case
            })

        current_line += 1

    logs['numberOfCorrectCases'] = correct
    print 'Correct results:' + str(correct)
    print ''
    print json.dumps(logs)

def f_enc(str):
    return str.decode('utf-8', 'ignore').encode('windows-1252', 'backslashreplace')


main()
