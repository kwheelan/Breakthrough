import os

writeFile = "textCode.html"
readFile = "CA_FAQS.txt"

numbers = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']

answers=[]
questions=[]
current = ''

f = open(readFile, 'r')

for line in f:
    line = line.strip()
    if line[:2] == "Q:":
        if current:
            answers.append(current)
        current = line[2:]
    elif line[:2] == "A:":
        questions.append(current)
        current = line[2:]
    else:
        if current:
            current += (line + "\n")

f.close()

f = open(writeFile, 'w')
f.write('<div id="accordion" align=left style = "margin-bottom: 30px">\n')

for n,a,q in zip(numbers, questions, answers):
    f.write('\t<div class="card faq">\n')
    f.write('\t\t<div class="card-header faqHeader" id="heading{}">\n'.format(n))
    f.write('\t\t\t<h4 class="mb-0">\n')
    f.write('\t\t\t\t<button class="btn btn-link sectLink" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" aria-controls="collapse{}">\n'.format(n,n))
    f.write('\t\t\t\t\t{}\n'.format(q))
    f.write('\t\t\t\t</button>\n')
    f.write('\t\t\t</h4>\n')
    f.write('\t\t</div>\n')
    f.write('\t</div>\n')
    f.write('\t<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" data-parent="#accordion">\n'.format(n,n))
    f.write('\t\t<div class="card-body">\n')
    f.write('\t\t\t{}\n'.format(a))
    f.write('\t\t</div>\n')
    f.write('\t</div>\n')

f.write('</div>')
f.close()
