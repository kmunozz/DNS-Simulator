import sys 

# function to read cache file
def read_cache(cache_filename):
    cache = []
    
    with open(cache_filename, 'r') as file:
        for line in file:
            cache.append(line.strip())
    return cache        


# function to write into cache
def write_cache(cache, cache_filename):
    with open(cache_filename, 'w') as file:
        for entry in cache:
            file.write(entry + '\n')


# function to update cache
def update_cache(cache, query):
    if query in cache:
        cache.remove(query)
    elif len(cache) == 3:
        cache.pop()
    cache.insert(0, query)        


# global variable
visited = []

# function to find TLD
def find_tld(query, cache):

    # declaring visited global
    global visited

    # Hard coded root file
    root_filename = '1-0-0-0.txt'

    # adding first file in visited lsit
    visited.append(root_filename)

    domain_info = {}  # Dictionary to store domain info

    # Opening root file
    with open(root_filename, 'r') as file:
        # Searching line by line 
        for line in file:
            # Splitting for domain and address
            info = line.strip().split(';')
            if len(info) == 2:
                domain = info[0]
                address = info[1]
                domain_info[domain] = [domain, address]

    # declaring new variables to get our next new address.txt
    edu_info = domain_info.get('edu')
    com_info = domain_info.get('com')
    gov_info = domain_info.get('gov')

    # looking at how the query ends '.edu' '.com' '.gov'
    query_domain = query.split('.')[-1]

    # finding TLD, going to function 
    if query_domain == edu_info[0]:
        visited.append(edu_info[1] + ".txt") # adding address to visited
        searching_edu(query, edu_info[1],cache)
        return
    elif query_domain == com_info[0]:
        visited.append(com_info[1] + ".txt") # adding address to visited
        searching_com(query, com_info[1],cache)
        return
    elif query_domain == gov_info[0]:
        visited.append(gov_info[1] + ".txt") # adding address to visited
        searching_gov(query, gov_info[1],cache)
        return
    else:
        print('Unresolved')
        return         



# Searching .edu
def searching_edu(query, address, cache):

    # begin with TLD .edu file
    dest_file = address + ".txt"

    #TESTING
    # print('made it into searching edu')

    # Variable to store the found entry
    found = None

    # Reading through file
    with open(dest_file, 'r') as file:
        for line in file:
            # Going to split the line to get domain & address
            domain, ip_address = line.strip().split(';')

            # TESTING
            # print("inside forloop domain:",domain)
            # print("ip address: ", ip_address)

            # found entry
            if query == domain:
                # print("I should not be in here")
                found = line.strip()  # Save the entire line
                break
            elif domain in query: # not found entry but the domain is in the query
                found = line.strip().split(';') # found domain thats in query, splitting to get address
                # print("Found:",found) # TESTING
                new_file = found[1] + ".txt"  # Variable to open new file
                visited.append(new_file)   # add new file to visited

                with open(new_file, 'r') as files:  # open new file
                    # print(new_file) TESTING
                    for inner_line in files: #Looking through new file
                        #Going to split the line to get domain & address
                        inner_domain, inner_ip_address = inner_line.strip().split(';')

                        # TESTING
                        # print("Inner-Domain:",inner_domain)
                        # print("Inner-ip:", inner_ip_address)

                        if query == inner_domain:
                            # print("hey I made it") # TESTING
                            found = inner_line.strip()  # Save the entire line
                            # print('FOUND:', found) # TESTING
                            break

    # Print visited files & entry found                        
    if found:
        visited.append(found.split(';')[-1])
        print(";".join([file.split('.')[0] for file in visited]))
        print(found)
        update_cache(cache, found)

    # if query not found
    if found==None:
        print("Unresolved")

    return


# Exact function as searching_edu, same comments 
def searching_com(query, address, cache):

    dest_file = address + ".txt"

    found = None

    with open(dest_file, 'r') as file:
        for line in file:
            # Going to split the line to get domain & address
            domain, ip_address = line.strip().split(';')


            if query == domain:
                # print("I should not be in here")
                found = line.strip()  # Save the entire line
                break
            elif domain in query:
                found = line.strip().split(';')
                # print("Found:",found)
                new_file = found[1] + ".txt"
                visited.append(new_file)

                with open(new_file, 'r') as files:
                    # print(new_file)
                    for inner_line in files:
                        # Going to split the line to get domain & address
                        inner_domain, inner_ip_address = inner_line.strip().split(';')

                        if query == inner_domain:
                            found = inner_line.strip()  # Save the entire line
                            break

    if found:
        visited.append(found.split(';')[-1])
        print(";".join([file.split('.')[0] for file in visited]))
        print(found)
        update_cache(cache, found)

    if found==None:
        print("Unresolved")    

    return


# Exact function as searching_edu, same comments 
def searching_gov(query, address, cache):    
    dest_file = address + ".txt"

    found = None

    with open(dest_file, 'r') as file:
        for line in file:
            # Going to split the line to get domain & address
            domain, ip_address = line.strip().split(';')

            if query == domain:
                # print("I should not be in here")
                found = line.strip()  # Save the entire line
                break
            elif domain in query:
                found = line.strip().split(';')
                new_file = found[1] + ".txt"
                visited.append(new_file)

                with open(new_file, 'r') as files:
                    # print(new_file)
                    for inner_line in files:
                        # Going to split the line to get domain & address
                        inner_domain, inner_ip_address = inner_line.strip().split(';')

                        if query == inner_domain:
                            # print("hey I made it")
                            found = inner_line.strip()  # Save the entire line
                            break

    if found:
        visited.append(found.split(';')[-1])
        print(";".join([file.split('.')[0] for file in visited]))
        print(found)
        update_cache(cache, found)

    if found==None:
        print("Unresolved")    

    return
 


def process_query(query, cache, cache_filename):    

    global visited

    print("Resolving query: " + query)

    visited = []

    # query_split = query.split('.')
    # query_domain = query_split[1]

    # first checking cache
    for entry in cache:
        if entry.split(';')[0] == query:
            # checking if query is in cache
            print("cache")
            print(entry)
            print('\n')

            # removing the current entry
            cache.remove(entry)
            # moving the current entry to top
            cache.insert(0,entry)
            # exiting the loops after finding query in cache
            break
    else:
        # if query isnt found in cache, call find tld
        find_tld(query, cache)

    print("\n")

    write_cache(cache, cache_filename)
        




def main(query_filename,cache_filename):
    
    # Reading cache from file
    cache = read_cache(cache_filename)

    # Reading file containing queries
    with open(query_filename, 'r') as file:
        # Reading line by line
        for line in file:
            # Removing whitespace
            query = line.strip()

            process_query(query, cache, cache_filename)

    
    print("\nCurrent cache:")
    for entry in reversed(cache):
        print(entry)


# Setting main arugments
if __name__ == "__main__":
    # Checking command-line for filenames, setting two arguements query and cache filenames
    if len(sys.argv) != 3:
        sys.exit(1)

    query_filename = sys.argv[1]
    cache_filename = sys.argv[2]

    main(query_filename, cache_filename)    
