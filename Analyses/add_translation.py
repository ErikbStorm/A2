import csv
from googletrans import Translator

def main():
    addTranslation()

def addTranslation():
    '''Reads a csv file and returns a list with lines.'''
    translator = Translator()

    with open('dataset.csv', 'r', newline="") as inf, open('dataset_trans.csv', 'w', newline="") as outf:
        csvreader = csv.DictReader(inf, delimiter=";")
        fieldnames = csvreader.fieldnames
        fieldnames[13]  = 'Translation'
        csvwriter = csv.DictWriter(outf, fieldnames=fieldnames, delimiter=";")
        csvwriter.writeheader()
        for line in csvreader:
            print(line['turntid'])
            sentence = line['Text'].replace('((NEWLINE))', ' ')

            if len(sentence) > 1:
                try:
                    sentence = translator.translate(sentence, src='nl', dest='en').text
                except:
                    sentence = line['Text'].replace('((NEWLINE))', ' ')
            line['Translation'] = sentence
            try:
                csvwriter.writerow(line)
            except:
                pass
if __name__ == '__main__':
    main()
