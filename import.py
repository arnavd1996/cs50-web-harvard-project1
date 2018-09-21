import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://pnrvnavoxvnlgw:4e404dad909373387cd7b0a473b85dce9f66dd1c344e7166f453efab0197c1c5@ec2-50-16-196-138.compute-1.amazonaws.com:5432/dc30a3q121n058')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None) #skip header on first row
    for isbn, title, author, year in reader:
        db.execute(
            "INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :publication_year)",
            {"isbn": isbn, "title": title, "author": author, "publication_year": year}
        )
    db.commit()

if __name__ == "__main__":
    main()
