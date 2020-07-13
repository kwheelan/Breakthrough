import os
import sys

writeFile = sys.argv[2]
readFile = sys.argv[1]

numbers = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
numbers = range(11)

answers=[]
questions=[]
current = ''

f = open(readFile, 'r')

for line in f:
    line = line.strip().replace('\n','')
    if line[:2] == "Q:":
        if current:
            questions.append(current)
        current = line[3:]
    elif line[:2] == "A:":
        answers.append(current)
        current = line[3:]
    else:
        if current and current != '\n':
            current += (" \n" + line)

f.close()

f = open(writeFile, 'w')
f.write('<div id="accordion2" align=left style = "margin-bottom: 30px">\n')

for n,a,q in zip(numbers, questions, answers):
    f.write('\t<div class="card faq">\n')
    f.write('\t\t<div class="card-header faqHeader" id="heading{}">\n'.format(n))
    f.write('\t\t\t<h4 class="mb-0">\n')
    f.write('\t\t\t\t<button class="btn btn-link collapsed sectLink" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">\n'.format(n,n))
    f.write('\t\t\t\t\t{}\n'.format(q))
    f.write('\t\t\t\t</button>\n')
    f.write('\t\t\t</h4>\n')
    f.write('\t\t</div>\n')
    f.write('\t\t<div id="collapse{}" class="collapse" aria-labelledby="heading{}" data-parent="#accordion2">\n'.format(n,n))
    f.write('\t\t\t<div class="card-body">\n')
    f.write('\t\t\t\t{}\n'.format(a))
    f.write('\t\t\t</div>\n')
    f.write('\t\t</div>\n')
    f.write('\t</div>\n')

f.write('</div>')
f.close()
