import random
import math
def correct_input(rate_books): 
    '''This function checks if the input is valid'''
    if rate_books == 0:
        return True
    elif rate_books % 2 == 0 or abs(rate_books) >  5:
        return False
    else:
        return True
def correct_input2(which_algorithm):
    '''This function takes which_algorithm input values ,detects if the user
    puts an improper input algorithm name'''
    if which_algorithm in ["A", "B", "C" ]:
        return True
    else:
        return False
passwords = {} #dictionary for the password; keys are new users, values are passwords
with open("passwords.txt", "r") as file:
    for line in file:
        x = line.strip().split(":") #splits the user and password with ":" symbol.
        passwords[x[0]] = x[1]
name_user = input("What is your name? ")
if name_user not in passwords.keys(): #if a new user appears
    print("Set your password, password can't include ':'")
    password = input()
    while ":" in password: #prompts the user for a password until the input is valid
        print("Please don't use the character ':'") #the ":" symbol is restricted
        password = input()
    passwords[name_user] = password
else:
    print("Enter your password")
    password = input()
    while password != passwords[name_user]: #prompts the user for a password until the correct password is given
        print("Wrong password, try again!")
        password = input()
line1 = "Before I can recommend some new books for you to read,\nyou need to tell me your opinion on a few books.\n"
line2 = "If you haven't read the book, answer 0 but use the scale\n -5 Hated it!\n -3 Didn't like it.\n 1 OK\n 3 Liked it.\n 5 Really liked it."
print(line1)
print(line2)
'''Reads the data in ratings.txt into the dict : customer_ratings'''
customer_ratings = {}
i = 0
with open("ratings.txt", "r") as file:
    name = ""
    data = [] #ratings from the fixed users
    for line in file:
        if i % 2 == 0:
            name = line.strip() #takes names from the ratings.txt
        else:
            data = list(map(int, line.strip().split(" ")))
            customer_ratings[name] = data
        i += 1

database_books = {} #books and average ratings
books = [] #list of all books
with open("books.txt", "r") as file:

    for line in file:
        database_books[line.strip()] = 0 #initialize with 0's
        books.append(line.strip())



keys = list(database_books.keys())
dont_recommend = [] #book list that won't get recommended to the user
random.shuffle(keys) #shuffles so that books are selected randomly
new_user = [0 for i in range(57)]
if name_user in customer_ratings.keys():
    new_user = customer_ratings[name_user] #Saves the rating returned by the user
'''Asks the user to rate 13 random books'''
for i in range(13):
    print(keys[i])
    rate_books = int(input())
    while not correct_input(rate_books):
        print("Try a valid rating number parallel to the scale!")
        rate_books = int(input())
    if rate_books != 0: #if book is already read, don't recommend
        dont_recommend.append(keys[i])
    index = books.index(keys[i])
    new_user[index] = rate_books
line3 = "I can make recommendations based on 3 different algorithms\nWhich algorithm? A, B or C"
print(line3)
which_algorithm = input() #prompts the user to pic an algorithm

while not correct_input2(which_algorithm):
    print("Please give a valid recommendation algorithm name!")
    which_algorithm = input()
print()
line4 = "Recommending based on Algorithm"
print(line4, str(which_algorithm))
print("++++++++++++++++++++++++++++++++++++")

def approach_A():
    ''' This function calculates and sorts the average ratings acording to high to low
    and recommends the highest 10 book to the user that the user hasn't read before'''
    for index, book in enumerate(database_books.keys()):
        sum = 0 #sum of ratings
        for ratings in customer_ratings.values():
            sum += ratings[index] #adds all the ratings to sum
        average = math.ceil(sum / len(customer_ratings)) #calculates rating average
        database_books[book] = average
    bookrating_pairs = list(database_books.items())
    bookrating_pairs.sort(key = lambda pair : pair[1], reverse = True) #sorts according to average ratings in decreasing order
    counter = 0
    for i in bookrating_pairs:
        if counter == 10: #stops when 10 books are printed
            break
        if i[0] not in dont_recommend: #if book is not previously read, recommends
            print(i[0])
            counter += 1


def approach_B(new_user):
    ''' This function finds the most similar customer to the new user, who is already present in the database
      and prints out  10 most rated books of the customer'''
    for  name, ratings in customer_ratings.items():
        similarity_total = 0 #sum of new user's ratings for each books times the customer's ratings for each book
        similarity = [] #stores each customer's sum
        counter = 0 #iterates over the ratings in new_user
        for i in ratings:
            x = i * new_user[counter] #dot product for each book
            counter += 1
            similarity_total += x
        similarity += [similarity_total]
    index = similarity.index(max(similarity)) #finds the highest sum's index in similarity list
    most_similar_user = list(customer_ratings.keys())[index] #finds the most similar user from the database according to index
    copy_books = books.copy() #copies books in order not to change the default book list
    copy_books.sort(key = lambda book : customer_ratings[most_similar_user][books.index(book)], reverse = True) #sorts the books according to the ratings of the most similar user
    for i in range(10):
        print(copy_books[i])


def approach_C(new_user):
    ''' This function calculates the dot product also combines that with all the customers
    and generates variety of  predictions that the highest 10 are recommended to the new user'''
    for name, ratings in customer_ratings.items():
        similarity_total = 0
        similarity = []
        a = 0
        for i in ratings:
            x = i * new_user[a]
            a += 1
            similarity_total += x
        similarity += [similarity_total]
        #same code until here in order to store the dot product just like in Approach B
    counter = 0
    customer_ratings_copy = customer_ratings.copy()
    for ratings in customer_ratings_copy.values():
        ratings = map(lambda rating : rating * similarity[counter], ratings) #adjust the rating according their similarities
        counter += 1
    predictions = [sum([customer_ratings_copy[name][i] for name in customer_ratings_copy.keys()]) for i in range(len(books))] #calculates predictions according to the given algorithm
    books_copy = books.copy()
    books_copy.sort(key=lambda book: predictions[books.index(book)], reverse=True) 
    for i in range(10):
        print(books_copy[i])
if which_algorithm == "A":
    approach_A()
elif which_algorithm == "B":
    approach_B(new_user)
else:
    approach_C(new_user)
customer_ratings[name_user] = new_user #adds new user's ratings to database
''' writes data back into the files'''
with open("ratings.txt", "w") as file:
    for name, ratings in customer_ratings.items():
        file.write(name + "\n")
        file.write(" ".join(map(str, ratings)) + "\n")
with open("passwords.txt", "w") as file:
    for name, password in passwords.items():
        file.write(name + ":" + password + "\n")









































































































