import csv
import re

matches_path = "Labelled Set G.csv"
matches_new_path = "matches.csv"
path_A = "TableA.csv"
path_B = "TableB.csv"
mergedFilePath = "Table E.csv"

matches_new = open(matches_new_path, "w", encoding='utf-8')
matches_new.write("tableA_title, tableA_author, tableB_title, tableB_author\n")
TableE = open(mergedFilePath, "w", encoding='utf-8')
TableE.write("title, author, rating, format\n")

# Open TableA and store in the form of dict for later traversal
tableA = {}
with open(path_A, newline='', encoding='utf-8') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    # Skips header
    next(rows)
    # Forms the dict
    for row in rows:
        tableA[row[0]] = [row[1], row[2], row[3], row[4]]

# Open TableB and store in the form of dict for later traversal
tableB = {}
with open(path_B, newline='', encoding='utf-8') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    # Skips header
    next(rows)
    # Forms the dict
    for row in rows:
        tableB[row[0]] = [row[1], row[2], row[3], row[4]]

'''
For each row in the Matches.csv file, go to the corresponding entries in TableA and TableB.
Then merge these two based on certain rules for each column.
Schema of TableE is same as TableA. And schema of TableA = schema of TableB
'''
with open(matches_path, newline='', encoding='utf-8') as csvfile:
    tuplePairs = csv.reader(csvfile, delimiter=',')
    # Skips header
    next(tuplePairs)
    for row in tuplePairs:
        # If label attribute of the row is 1, then it is a correct match and merge this entry in the new TableE
        if (int(row[8]) == 1):

            # Write this matching entity in a new table. (For submission only)
            matches_new.write(row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + '\n')

            dataA = tableA[row[2]]
            dataB = tableB[row[3]]

            # Selecting title based on length. Choosing the bigger length title.
            if (len(dataA[0]) >= len(dataB[0])):
                title = dataA[0]
            else:
                title = dataB[0]
            title = re.sub('[,]', '', title)

            # Selecting author based on length. Choosing the one with smaller length.
            if (len(dataA[1]) <= len(dataB[1]) or len(dataB[1]) == 0):
                author = dataA[1]
            else:
                author = dataB[1]

            # Selecting the rating based on average of the two.
            # Few values of rating are empty in TableB.
            if (dataB[2] == ''):
                rating = float(dataA[2])
            else:
                 rating = (float(dataA[2]) + float(dataB[2]))/2

            # Selecting the format based on TableA as it is more reliable source than TableB.
            format = dataA[3]

            # Writing to TableE
            TableE.write(title + ',' + author + ',' + '{0:.2f}'.format(rating) + ',' + format + '\n')