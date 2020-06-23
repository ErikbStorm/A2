import csv


def main():
    data = importData("dataset.csv")
    analyzeTime(data)


def analyzeTime(data):
    matrix = {}

    for line in data:
        if line['Duration'] != '':
            try:
                matrix[line['INTERFACEUSED']] += [float(line['Duration'])]
            except KeyError:
                matrix[line['INTERFACEUSED']] = [float(line['Duration'])]
            except ValueError:
                pass

    matrix = {k: sum(v)/len(v) for k, v in matrix.items()}

    print(matrix)


def importData(loc):
    f = open(loc, 'r', newline="")
    reader = csv.DictReader(f, delimiter=";")
    # f.close()
    return reader


if __name__ == '__main__':
    main()
