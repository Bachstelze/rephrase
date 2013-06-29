
import json

def main():

    f = open('en2.out')
    en2_lines = f.readlines()
    f.close()

    f = open('ru.out')
    ru_lines = f.readlines()
    f.close()

    f = open('en.orig.in')
    en_lines = f.readlines()
    f.close()

    align_data = {}
    for i, en2 in enumerate(en2_lines):
        align_data[str(i+1)] = align(en_lines[i], ru_lines[i], en2)

    print json.dumps(align_data)

#    en = 'indiana was the first state to impose such a requirement .'
#    ru = 'indiana |0-0| stala pervym |1-3| gosudarstvom |4-4| navjazat |5-6| takoe trebovanie . |7-10|'
#    en2 = 'indiana |0-0| became the |1-1| first state |2-3| to impose |4-4| such a requirement . |5-7|'

def align(en, ru, en2):

    alignment_results = []

    en2_parsed = parse(en2)
    ru_parsed = parse(ru)

    orig_cov = get_orig_cov(en2_parsed, ru_parsed)

    c_arr = []
    o_arr = []

    for i, cov in enumerate(en2_parsed['coverage']):
        original = ''
        for c in orig_cov[i]:
            original += ' ' + get_cov(c, en).strip()

        original = original.strip()
        corrupted = en2_parsed['tokens'][i].strip()

        if corrupted != original:
            # new phrase mismatch

            if len(c_arr) == 0:
                c_arr.append([])
                o_arr.append([])
            else:
                if (len(orig_cov[i]) > 0) and (len(orig_cov[i-1]) > 0):
                    cur_first_cov = orig_cov[i][0]
                    prev_first_cov = orig_cov[i-1][0]
                    h = cov_split(cur_first_cov)['start']
                    t = cov_split(prev_first_cov)['end']-1
                    if h <= t:
                        c_arr.append([])
                        o_arr.append([])


            c_arr[len(c_arr) - 1].append(corrupted)
            o_arr[len(o_arr) - 1].append(original)

    for i, c_arr_item in enumerate(c_arr):
        c_out = ' '.join(c_arr_item).strip()
        o_out = ' '.join(o_arr[i]).strip()
        if c_out != o_out:
            alignment_results.append({
                'corrupted': c_out,
                'original': o_out
            })

    return alignment_results


def get_cov(cov, str):
    str_parts = str.split(' ')
    pcov = cov_split(cov)
    return ' '.join(str_parts[pcov['start']:(pcov['end']+1)])

def get_orig_cov(en2_parsed, ru_parsed):
    result = []
    for i, cov in enumerate(en2_parsed['coverage']):
        parsed_cov = cov_split(cov)
        orig_cov = []

        ru_head = 0
        ru_words = 0

        while parsed_cov['start'] > ru_words:
            ru_words += get_words_count(ru_parsed['tokens'][ru_head])
            ru_head += 1


        while (parsed_cov['start'] <= ru_words) and (parsed_cov['end'] >= ru_words):
            orig_cov.append(ru_parsed['coverage'][ru_head])
            ru_words += get_words_count(ru_parsed['tokens'][ru_head])
            ru_head += 1

        result.append(orig_cov)

    return result

def cov_split(cov):
    cov_parts = cov.split('-')
    cov_start = int(cov_parts[0])
    cov_end = int(cov_parts[1])
    return {
        'start': cov_start,
        'end': cov_end
    }

def get_words_count(str):
    return len(str.strip().split(' '))

def parse(str):
    str_parts = str.split('|')
    x = True
    tokens = []
    coverage = []
    for part in str_parts:
        if x:
            tokens.append(part)
        else:
            coverage.append(part)
        x = not x

    return {
        'tokens': tokens,
        'coverage': coverage
    }



main()