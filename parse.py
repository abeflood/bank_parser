import csv
import os
import sys
import getopt
from datetime import datetime
import operator

def main(argv):
    #create consts
    Outputfilename = 'Results.csv'
    directory = 'bank-files'
    date_string = 'Transaction Date'
    name_string = 'Description'
    amount_string = 'Transaction Amount'
    outputTitles = [date_string, name_string, amount_string]

    try:
      opts, args = getopt.getopt(argv,"h:d:f:")
    except getopt.GetoptError:
      print('Use the following format -> parse.py -f <filename-to-save-results> -d <input-files-directory>')
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Use the following format -> parse.py -f <filename-to-save-results> -d <input-files-directory>')
            sys.exit()
        elif opt in ("-d"):
            directory = arg
        elif opt in ("-f"):
            Outputfilename = arg

    #Iterate through all files in directory
    allRecords = list()
    titles = list()

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            with open(os.path.join(directory, filename)) as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if len(row) > 1: #Get rid of empty rows and title row
                        if row[0] == 'Item #':
                            if len(titles) == 0:
                                for title in row:
                                    titles.append(title)
                        else:
                            record = dict()
                            for num, item in enumerate(row):
                                record[titles[num]] = item
                            allRecords.append(record)

    #Make changes to records
    for record in allRecords:
        #todo add categories automatically
        #change date format
        datetimeobject = datetime.strptime(record[date_string],'%Y%m%d')
        record[date_string] = datetimeobject.strftime('%m-%d-%Y')
        record['datetime'] = datetimeobject
    
    #sort by date
    allRecords = sorted(allRecords, key=operator.itemgetter('datetime'))

    #Make output file
    with open(Outputfilename, 'w', newline='') as csvfile:
        #write ouput file
        writer = csv.DictWriter(csvfile, fieldnames=outputTitles, extrasaction='ignore')
        writer.writeheader()
        for record in allRecords:
            writer.writerow(record)
        csvfile.close()
                        
if __name__ == "__main__":
   main(sys.argv[1:])