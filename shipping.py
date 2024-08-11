# dictionaries for all the available providers for each size and the cost
small = {
    "LP": 1.5,
    "MR": 2
}

medium = {
    "LP": 4.9,
    "MR": 3
}

large = {
    "LP": 6.9,
    "MR": 4
}

# global variables that are subject to change
current_month = 0  # initialiser for current month
max_count = 3      # what number shipment should be free for L via LP
large_count = 1    # number of L via LP shipments made
max_discount = 10  # maximum discounts per month
current_discount = 0   # accumulated discount


# read in each line from the file and calculate the transaction
def readFile():
    with open("input.txt", "r") as file:
        for line in file:
            line = line.strip()
            addTransaction(line)

# calculate transaction and write to output file
def addTransaction(line):
    # access global variables so they can be changed
    global current_month, large_count, current_discount
    
    # sort prices for small providers to access smallest provider price
    sorted_small = dict(sorted(small.items(), key=lambda item: item[1]))
    line_split = line.split(" ")    # split line by spaces to get value of each line
    size = line_split[1]       # get the size of the order 
    
    month = int(line_split[0].split("-")[1])   # get the month of the order
    
    # if its a new month, reset all the global variables
    if month != current_month:
        current_month = month
        large_count = 1 
        current_discount = 0
    
    # if all the values are available in the line and are recognized, calculate the transaction otherwise ignore
    if (len(line_split) == 3):
        provider = line_split[2]

        if size == "S":
            if provider in small:
                key, value = next(iter(sorted_small.items()))  # get smallest value
                transaction, discount = calculate_discount(sorted_small[provider], value)   # calculate discount
                write_line = create_line(line, transaction, discount)  # create the line to write to file
            else:
                write_line = line + " Ignored"    # create the line to write to file
                 
        elif size == "M":
            if provider in medium:
                transaction = medium[provider]
                discount = 0
                write_line = create_line(line, transaction, discount)   # create the line to write to file
            else:
                write_line = line + " Ignored"    # create the line to write to file
        elif size == "L":
            if provider == "LP":
                if large_count == max_count:   # if the number of L via LP has reached the 3rd order
                    transaction, discount = calculate_discount(large[provider], 0)  # calculate discount
                    large_count += 1
                else:
                    transaction = large[provider]
                    discount = 0
                    large_count += 1
                write_line = create_line(line, transaction, discount)    # create the line to write to file
            elif provider in large:
                transaction = large[provider]
                discount = 0
                write_line = create_line(line, transaction, discount)    # create the line to write to file
            else:
                write_line = line + " Ignored"     # create the line to write to file
        else:
            write_line = line + " Ignored"    # create the line to write to file
            
    else:
        write_line = line + " Ignored"    # create the line to write to file
    
    
    # print to terminal and write to file
    print(write_line)
    with open("output.txt", "a") as file:
        file.write(write_line + "\n")


# create formatting for writing to file
def create_line(line, transaction, discount):
    global current_discount
    transaction = f"{transaction:.2f}"
    if discount == 0:
        discount = "-"
    else:
        current_discount += discount
        discount = f"{discount:.2f}"
        
    write_line = line + " " + str(transaction) + " " + str(discount)
    return write_line


# calculate the discount depending on available discount values
def calculate_discount(provider_price, transaction):
    discount = provider_price - transaction   # apporximated discount
    
    if max_discount - current_discount >= discount:
        return transaction, discount   # if there is enough money, approx. discount can be applied
    discount = max_discount - current_discount   # if there isnt enough money, recalculate discount based on what is left
    transaction = provider_price - discount   # recalculate transaction based on new discount
    return transaction, discount
        
readFile()

