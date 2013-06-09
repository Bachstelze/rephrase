

def main():
    f = open('4.graph')
    lines = f.readlines()

    hyps = process_lines(lines)
    f.close()

    print hyps[0]
    print hyps[1]
    print hyps[2]
    print hyps[3]
    print hyps[4]
    print hyps[5]
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

    return hyp

main()

#
#import sqlite3
#
#conn = sqlite3.connect('example.db')
#
#c = conn.cursor()
#
## Create table
#c.execute('''CREATE TABLE stocks
#             (date text, trans text, symbol text, qty real, price real)''')
#
## Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#
## Save (commit) the changes
#conn.commit()
#
## We can also close the connection if we are done with it.
## Just be sure any changes have been committed or they will be lost.
#conn.close()