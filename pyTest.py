import csv
with open('/home/dth/IDEA Projects/VorTidsMusik/kanalnavne.csv', 'rb') as f:
    reader = csv.reader(f)
    rownum = 0
    for row in reader:# Save header row.
        if rownum == 0:
            header = row
        else:
            if True:
                id = row[0]  
                titel = row[1]
                kanalnavn = row[3]
                findesIkke = row[4]

                print "Id: "+id
                print "Titel: "+titel
                print "Kanalnavn: "+kanalnavn
                print "Findes ikke: "+findesIkke
        rownum += 1
