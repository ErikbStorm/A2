import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main():
    data = importData("dataset.csv")
    analyzeTime(data)
    # analyzeTurnTaking(data)
    # analyzeLanguage(data)
    # analyzeDataconsumption(data)
    # analyseHappiness(data)
    # analyseEmotion(data)


def analyzeDataconsumption(data):
    '''Analyze the difference in data usage between the two systems.'''
    matrix = {'WYSIWYG': [], 'TBT': []}
    for line in data:
        length = len(line['Text'].replace('((NEWLINE))', ' '))
        try:
            matrix[line['INTERFACEUSED']].append(length)
        except KeyError:
            pass

    matrix = {k: round(sum(v)/len(v), 2) for k, v in matrix.items()}
    print(f"Average chars sent per line for each interface: {matrix}")


def analyzeLanguage(data):
    '''Overlap in words measured between systems.'''
    overlap = {'WYSIWYG': [], 'TBT': []}
    last_part = ''
    last_interface = ''
    last_words = []
    words = []
    for line in data:
        part = line['Sender']
        interface = line['INTERFACEUSED']
        words += line['Text'].split()
        if interface == last_interface:
            if last_part == part:
                pass
            else:
                overlap[interface].append(
                    getOverlapWordCounts(last_words, words))
                last_words = words
                words = []
        else:
            last_interface = interface
            last_words = words
            words = []

    overlap = {k: (sum(v)/len(v))*100.0 for k, v in overlap.items()}
    print(f"% of overlap between per turn: {overlap}")


def getOverlapWordCounts(text1, text2):
    '''Counts the overlapping words between interfaces.'''
    overlap_count = 0
    for word in text1:
        if word in text2:
            overlap_count += 1
    return overlap_count


def analyzeTurnTaking(data):
    '''Analyzes the average amount of messages before the other participant intervenes.'''
    avg_turns = {'WYSIWYG': [], 'TBT': [], '': []}

    last_interface = ''
    last_part = ''
    count = 1
    for line in data:
        if last_interface == line['INTERFACEUSED']:
            if last_part == line['Sender']:
                count += 1
            else:
                avg_turns[line['INTERFACEUSED']].append(count)
                last_part = line['Sender']
                count = 1
        else:
            avg_turns[line['INTERFACEUSED']].append(count)
            last_interface = line['INTERFACEUSED']
            count = 1

    avg_turns = {k: sum(v)/len(v) for k, v in avg_turns.items()}
    print(f"Average messages per turn: {avg_turns}")


def analyzeTime(data):
    '''Average time of a game between interfaces.'''
    matrix = {"WYSIWYGTBT": {}, "TBTWYSIWYG": {}}

    last_gameno = 0
    time = 0
    game_count = 1
    for line in data:
        gameno = line['GameNo']
        if line['INTERFACEUSED'] == "TBT":
            interface = "WYSIWYG"
        elif line['INTERFACEUSED'] == "WYSIWYG":
            interface = "TBT"
        if line['experimenttype'] == "WYSIWYGTBT":
            ex_type = "TBTWYSIWYG"
        elif line['experimenttype'] == "TBTWYSIWYG":
            ex_type = "WYSIWYGTBT"
        if gameno == last_gameno:
            if line['Duration'] != '':
                try:
                    time += int(line['Duration'])
                except:
                    pass
        else:
            game_count += 1
            try:
                matrix[ex_type][interface] += [time]
            except KeyError:
                matrix[ex_type][interface] = [time]
            time = 0
            last_gameno = gameno

    print(matrix)

    writeToCSV(matrix)

    print(game_count)
    print(f"Average time for a game for each interface: {matrix}")


def writeToCSV(dicto):
    with open("lengths.csv", "w+", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            ["experiment_type", "Interface_used", "gameid", "game_length"])
        i = 0
        for k, v in dicto.items():
            for kk, vv in v.items():
                for num in vv:
                    i += 1
                    writer.writerow([k, kk, i, num])


def analyseHappiness(data):
    '''Average positive sentiment per line per interface type'''
    matrix = {}
    sid = SentimentIntensityAnalyzer()

    for line in data:
        if line['INTERFACEUSED'] in ['WYSIWYG', 'TBT']:

            sentence = line['Text'].replace('((NEWLINE))', ' ')
            ss = sid.polarity_scores(sentence)

            try:
                matrix[line['INTERFACEUSED']]['sum'] += ss['pos']
                matrix[line['INTERFACEUSED']]['total'] += 1
            except KeyError:
                matrix[line['INTERFACEUSED']] = {}
                matrix[line['INTERFACEUSED']]['sum'] = ss['pos']
                matrix[line['INTERFACEUSED']]['total'] = 1

    for type in matrix:
        average = matrix[type]['sum'] / matrix[type]['total']
        print(f'Average happiness per line for {type}: {average}')


def analyseEmotion(data):
    '''Average time of a game between interfaces.'''
    matrix = {}
    sid = SentimentIntensityAnalyzer()
    previous_emotion = ''
    previous_type = ''

    for line in data:
        if line['INTERFACEUSED'] in ['WYSIWYG', 'TBT']:

            sentence = line['Text'].replace('((NEWLINE))', ' ')
            ss = sid.polarity_scores(sentence)

            if ss['neg'] < ss['pos']:
                current_emotion = 'pos'
            else:
                current_emotion = 'neg'

            try:
                matrix[line['INTERFACEUSED']]['total'] += 1
            except KeyError:
                matrix[line['INTERFACEUSED']] = {}
                matrix[line['INTERFACEUSED']]['total'] = 1

            if current_emotion != previous_emotion:
                try:
                    matrix[line['INTERFACEUSED']]['sum'] += 1
                except KeyError:
                    matrix[line['INTERFACEUSED']]['sum'] = 1

            if previous_type != line['INTERFACEUSED']:
                try:
                    matrix[line['INTERFACEUSED']]['sum'] -= 1
                except:
                    pass

            previous_emotion = current_emotion
            previous_type = line['INTERFACEUSED']

    for type in matrix:
        average = matrix[type]['sum'] / matrix[type]['total']
        print(f'Average emotional change per line for {type}: {average}')


def importData(loc):
    '''Reads a csv file and returns a list with lines.'''
    with open(loc, 'r', newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        dicto = [line for line in reader]
    return dicto


if __name__ == '__main__':
    main()
