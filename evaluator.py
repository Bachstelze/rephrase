
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
    for line in en2_out_lines:
        if current_line < 16:
            current_line += 1
            continue
        if current_line > 516:
            break
        print 'Testing sentence #' + str(current_line)
        test_pairs = align_data[str(current_line)]
        for test_pair in test_pairs:
            N = 55
            paraphrases = rephraser.rephrase(line, test_pair['corrupted'], '../../evaluation/graph-dbs/s' + str(current_line-1) + '.graph.db', N)
        #    print 'corrupted: ' + test_pair['corrupted']
        #    print 'original: ' + test_pair['original']
            for paraphrase in paraphrases:
        #        print paraphrase
                if test_pair['original'].strip() == paraphrase.strip():
                    correct += 1
                    break
        current_line += 1

    print 'Correct results:' + str(correct)

main()
