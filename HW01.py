########
#Part 1#
########

# Replace the pass with your code according to the instructions in the HW01 Prompt
# You can use the test cases at the bottom in order to test your code

def add_digits(int_list):
    newStr = ""
    for i in int_list:
        newStr += str(i)

    return int(newStr)

def string_modifier(str_list):
    newList = []
    for i in str_list:
        if i.islower() and i.isalpha():
            a = i * (len(i))
            newList.append(a)
    return newList

def contacts(phone_numbers):
    count = 0
    newlist = []
    for i in phone_numbers:
        temp_str = ""
        for l in i:
            if l.isdigit() == True:
                temp_str += str(l)
        if len(temp_str) == 10 and temp_str[0:3] == "404" and temp_str not in newlist:
            count += 1
            newlist.append(temp_str)
    
    return count

def shelf_books(book_list):
    return [i[0] for i in sorted(book_list, key=lambda name: name[1].split()[-1])]

def classics(books, chapters, authors): # check if this works
    return {book:(True if (author != "J. Joyce" and chap >= 20) else False) for book, chap, author in list(zip(books, chapters, authors))}

def writers(authors, age_at_death):
    return {index+1: tup[0] for index, tup in enumerate(sorted(list(zip(authors, age_at_death)), key=lambda age: age[1], reverse = True))}

########
#Part 2#
########

# Create the Book and Library classes below as specified by the HW01 prompt
# You will need to use the correct function/method names!

class Book:
    def __init__(self, name, genre, year, pages):
        self.name = name # str
        self.genre = genre # str
        self.year = year # int
        self.pages = pages # int
    
    def __lt__(self, other):
        return self.year < other.year
    
    def __eq__(self, other):
        return self.name == other.name and self.year == other.year and self.pages == other.pages

    def __repr__(self):
        return f"{self.name} is a {self.pages} pages long {self.genre} book published in {self.year}."


class Library:
    def __init__(self, name, book_list):
        self.name = name # str
        self.book_list = [Book(x[0], x[1], x[2], x[3]) for x in book_list] # list
        self.num_fiction = "0" # str

        for i in book_list:
            if i[1] == "Fiction":
                self.num_fiction = int(int(self.num_fiction) + 1)

    def __repr__(self):
        return f"{self.name} is a library where {str(self.num_fiction)} of the {str(len(self.book_list))} books are fiction."
    
    def __lt__(self, other):
        return int(self.num_fiction) < int(other.num_fiction)

    def add_book(self, new_book):
        self.book_list.append(Book(new_book[0], new_book[1], new_book[2], new_book[3]))

        if new_book[1] == "Fiction":
            self.num_fiction = int(int(self.num_fiction) + 1)

        


if __name__ == '__main__':
    #********************************************************************************************************************
    # Uncomment the necessary lines below to test specific functions and classes in command line or terminal            #
    # After you test your functions, MAKE SURE TO RE-COMMENT OUT ALL PRINT STATEMENTS BEFORE SUBMITTING IN GRADESCOPE   #
    #********************************************************************************************************************

    # Part 1: test add_digits
    int_list = [1, 4, 3, 8, 1]
    # print(add_digits(int_list))

    # Part 1: test string_modifier
    str_list = ['ace', 'BLuE42', 'b4a', 'cs']
    # print(string_modifier(str_list))

    # Part 1: test contacts
    phone_numbers = ['4o04592,,,0000', '-%#3&0&3!0', '4!0!4!5!9!2!0!0!0!0!','908',
                     '4###04...-,,,,,78', '404$$$193--8173', '3^^0--,30']
    # print(contacts(phone_numbers))

    # Part 1: test shelf_books
    book_list = [('It', 'Stephen King'), ('Gone Girl', 'Gillian Flynn'), ('Verity', 'Colleen Hoover')]
    # print(shelf_books(book_list))

    # Part 1: test classics
    books = ['Around the Moon', 'Ulysses', '1984', 'Don Quixote']
    books2 = ['Frankenstein', 'Araby','Doctor Sleep']
    chapters = [25, 45, 12, 90]
    chapters2 = [30, 1, 20]
    authors = ['J. Verne', 'J. Joyce', 'G. Orwell', 'M. Cervantes']
    authors2 = ['M. Shelley', 'J. Joyce', 'S. King']
    # print(classics(books2, chapters2, authors2))

    # Part 1: test writers
    authors = ['J. Swift', 'T. Paine', 'C. Dickens', 'H. Melville']
    age_at_death = [78, 73, 58, 72]
    # print(writers(authors, age_at_death))

    # Part 2: Class 1
    # Book1 = Book('Normal People', 'Fiction', 2018, 273) 
    # Book2 = Book('The Catcher in the Rye', 'Fiction', 1951, 234)
    # Book3 = Book('Normal People', 'Some unknown genre', 2018, 273) 
    # print(Book1.name)
    # print(Book1.genre)

    # print(Book1 < Book2)

    # print(Book1 == Book2)  
    # print(Book1 == Book3) 

    # print(Book1) 

    # Part 2: Class 2
    book_list = [['Normal People', 'Fiction', 2018, 273],
                 ['The Catcher in the Rye', 'Fiction', 1951, 234],
                 ['The Goal', 'Fiction', 1984, 384],
                 ['How to Think Like a Computer Scientist', 'Textbook', 2002, 274]]
    # Bohongs_Library = Library('Bohong’s Books', book_list)
    # print(Bohongs_Library.name)

    # print(Bohongs_Library)

    # Erins_Library = Library('Erin’s Excellent Essays',[['Arriving Today: From Factory to Front Door', 'Nonfiction', 2021, 384]])
    # print(Bohongs_Library < Erins_Library)
 
    book1 = ['The Hunger Games', 'Fiction', 2008, 374]
    # Bohongs_Library.add_book(book1)
    # print(Bohongs_Library)