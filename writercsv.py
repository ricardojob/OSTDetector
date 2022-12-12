import csv
from datetime import datetime

class WriterCSV:
  def __init__(self, name, path='data-csv'):
    self.name = name
    # self.dir= "test"
    self.path = path

  def write(self, head, rows):
    csv_filename = f"{self.path}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{self.name}.csv"
    with open(csv_filename, 'w') as file:
        # write = csv.writer(file, delimiter =";",quoting=csv.QUOTE_NONNUMERIC)
        write = csv.writer(file, delimiter =";")
        write.writerow(head)
        write.writerows(rows)