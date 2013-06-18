
def main():
    f = open('en2.out')
    lines = f.readlines()

    out = ''
    for line in lines:
        out += process_line(line)

    f.close()

    o = open('en2.out.p', 'w')
    o.write(out)
    o.close()
    pass

def process_line(line):
    line_parts = line.split('|')

    result = ''
    x = True
    for part in line_parts:
        if x:
            result += part
        x = not x

    return result

main()