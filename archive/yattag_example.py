from yattag import Doc

doc, tag, text = Doc().tagtext()

with tag('html'):
    with tag('body'):
        with tag('h1'):
            text('Last reported cases in a day')
        with tag('h2'):
            text('Toronto')
        with tag('h3'):
            text('Cases: ' + str(10))
        with tag('h3'):
            text('Percentage of population: ' + str(0.005) + '%')
        doc.stag('br')

with open('test.html', 'w') as writer:
    writer.write(doc.getvalue())