
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
                if calculateDistance(test_pair['original'].strip(), paraphrase.strip()) < 4:
                    correct += 1
                    correct_case = True
                    break
            logs['tests'].append({
                'lineNo': current_line,
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


def zeros(x, y):
    result = []
    for i in range(0, y):
        row = []
        for j in range(0, x):
            row.append(0)
        result.append(row)
    return result

def calculateDistance(word1, word2):
    x = zeros( (len(word1)+1, len(word2)+1) )
    for i in range(0,len(word1)+1):
        x[i,0] = i
    for i in range(0,len(word2)+1):
        x[0,i] = i

    for j in range(1,len(word2)+1):
        for i in range(1,len(word1)+1):
            if word1[i-1] == word2[j-1]:
                x[i,j] = x[i-1,j-1]
            else:
                minimum = x[i-1, j] + 1
                if minimum > x[i, j-1] + 1:
                    minimum = x[i, j-1] + 1
                if minimum > x[i-1, j-1] + 1:
                    minimum = x[i-1, j-1] + 1
                x[i,j] = minimum

    return x[len(word1), len(word2)]

main()
