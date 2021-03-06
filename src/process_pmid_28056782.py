#!/usr/bin/env python3

import io
import csv
import openpyxl
import utils


def download():
    utils.download_file('https://static-content.springer.com/esm/art%3A10.1186%2Fs12859-016-1415-9/MediaObjects/' +
                        '12859_2016_1415_MOESM1_ESM.xlsx', '../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.xlsx')


def convert_to_csv():
    workbook = openpyxl.load_workbook('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.xlsx')
    sheet = workbook.get_sheet_by_name('ensemble method')
    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.csv', 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f)
        for r in sheet.rows:
            c.writerow([cell.value for cell in r])


def deduplicate():
    result = []
    matched = set()
    duplicated = 0

    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.csv', 'r', encoding='utf-8') as f:
        # Drug ID1,Drug ID2,Drug Name1,Drug Name2,Confirm?
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            row = [x.strip() for x in row]
            # Skip unconfirmed
            # if row[4] == 'False':
            #     continue
            id1 = row[0]
            id2 = row[1]
            id_key = '%s:%s' % (id1 if id1 < id2 else id2, id2 if id1 < id2 else id1)
            if id_key not in matched:
                matched.add(id_key)
                result.append(row)
            else:
                duplicated += 1

    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM_unique.csv', 'w', newline='',
                 encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['Drug ID1', 'Drug ID2', 'Drug Name1', 'Drug Name2', 'Confirmed'])
        for row in result:
            writer.writerow(row)

    # Matched, Duplicated, Unmatched
    return [len(result), duplicated, 0]


def process() -> [int]:
    convert_to_csv()
    return deduplicate()


def get_all_interaction_pairs() -> []:
    result = []
    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM_unique.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            # Ignore confirmed value due to the fact we can check existence in DrugBank directly
            result.append([row[0], row[2], row[1], row[3], -1])
    return result
