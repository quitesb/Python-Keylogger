# The purpose of this code is only to learn how a keylogger works in the context of cybersecurity
 
# Objective 1: learn how to store the keystrokes actually typed in a txt file
# Objective 2: pratice file handling, how to read and append to a file   

# to read a file in python  I will use this function
# the first parameter is the name of the file and the second the mode
# mode can be: r (read) ; w (write) ; a (append) ; rb (read binary) ; x (exclusive creation)
# if the file doesnt exists, the function will create 


# the function open() returns a file object that can be manipulated
file = open("hello.txt", 'w')
file.write ("Hello World")

# closing the file is important to avoid memory leaks in some situations
file.close()

# the difference between the 'r' and 'a' parameters: 'r' always overwrites the file, while 'a' appends the content to the end of the file.
# the append dont break a line, use \n for this
file = open("hello.txt", 'a')
file.write("!\n")
file.close()

# using the r mode and printing
file = open("hello.txt", 'r')
file_data = file.read()
# print(file_data), uncomment for print
file.close()


# Using the keyword with we can open a file with more securety
# close() is auto called

with open("hello.txt", 'a') as file: 
    file.write("Hello again!")
    