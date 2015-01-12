import MySQLdb

def main():
  # db = MySQLdb.connect('oniddb.cws.oregonstate.edu', 
  #                      'felll-db',
  #                      'Qo8KoTmgkOUFj7bs', 
  #                      'felll-db')
  # cur = db.cursor()
  target = open('pyfile', 'w+')
  target.write("my py info")
  target.close()

if __name__ == '__main__':
  main()
