#Dijkstra solution
import sys, time

def print_the_results(number_of_A, number_of_B, elapsed_time, fastest_solution, final_route):
    print("The smallest time needed from A(" + str(number_of_A) + ") to B(" + str(number_of_B) + ") = " + str(fastest_solution))
    print("route: " + str(final_route))
    print("Elapsed time: ", elapsed_time)

def split_originall_field(file_content, NUM_ROWS):
    first_field_withSymbols = []
    second_field_withSymbols = []
    for i in range(0, 2 * NUM_ROWS + 1):
        if file_content[i] == "":
            continue
        if i < NUM_ROWS:
            first_field_withSymbols.append(file_content[i])
        else:
            second_field_withSymbols.append(file_content[i])
    return first_field_withSymbols, second_field_withSymbols

def define_field(NUM_ROWS, NUM_COLUMNS, first_field_withSymbols, second_field_withSymbols):
    FIELD_SIZE = NUM_ROWS * NUM_COLUMNS
    FIELD = [[] for i in range(0, 2 * FIELD_SIZE)]
    currentCounter = 0
    for i in range(0, NUM_ROWS):
        for j in range(0, NUM_COLUMNS):
            if first_field_withSymbols[i].find('A') != -1:
                if not COORDINATES_A:
                    COORDINATES_A.append(first_field_withSymbols[i].find('A'))
                    COORDINATES_A.append(i)
            if first_field_withSymbols[i].find('B') != -1:
                if not COORDINATES_B:
                    COORDINATES_B.append(first_field_withSymbols[i].find('B'))
                    COORDINATES_B.append(i)
            
            if first_field_withSymbols[i][j] == '.' or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B':
                #left
                if first_field_withSymbols[i][j - 1] == '.' or first_field_withSymbols[i][j - 1] == 'A' or first_field_withSymbols[i][j - 1] == 'B':
                    #ind = currentCounter - 1
                    FIELD[currentCounter].append(currentCounter - 1)
                #right
                if j + 1 < len(first_field_withSymbols[i]) and (first_field_withSymbols[i][j + 1] == '.' or first_field_withSymbols[i][j + 1] == 'A' or first_field_withSymbols[i][j + 1] == 'B'):
                    #ind = currentCounter + 1
                    FIELD[currentCounter].append(currentCounter + 1)
                
                #top
                if first_field_withSymbols[i - 1][j] == '.' or first_field_withSymbols[i - 1][j] == 'A' or first_field_withSymbols[i - 1][j] == 'B':
                    ind = (NUM_COLUMNS * (i - 1)) + j
                    FIELD[currentCounter].append(ind) 
                
                #bottom
                if first_field_withSymbols[i + 1][j] == '.' or first_field_withSymbols[i + 1][j] == 'A' or first_field_withSymbols[i + 1][j] == 'B':
                    ind = (NUM_COLUMNS * (i + 1)) + j
                    FIELD[currentCounter].append(ind) 
                    
                #teleport
                if second_field_withSymbols[i][j] == '.':
                    FIELD[currentCounter].append(currentCounter + (FIELD_SIZE)) 
            #for second field
            if second_field_withSymbols[i][j] == '.':
                #left
                if second_field_withSymbols[i][j - 1] == '.':
                    FIELD[currentCounter + (FIELD_SIZE)].append(currentCounter - 1 + (FIELD_SIZE))
                
                #right
                if j + 1 < len(second_field_withSymbols[i]) and second_field_withSymbols[i][j + 1] == '.':
                    FIELD[currentCounter + (FIELD_SIZE)].append(currentCounter + 1 + (FIELD_SIZE))
                
                #top
                if second_field_withSymbols[i - 1][j] == '.':
                    ind = (NUM_COLUMNS * (i - 1)) + j
                    FIELD[currentCounter + (FIELD_SIZE)].append(ind + (FIELD_SIZE))
                
                #bottom
                if i + 1 < len(second_field_withSymbols) and second_field_withSymbols[i + 1][j] == '.':
                    ind = (NUM_COLUMNS * (i + 1)) + j 
                    FIELD[currentCounter + (FIELD_SIZE)].append(ind + (FIELD_SIZE))
                    
                #teleport
                if first_field_withSymbols[i][j] == '.' or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B':
                    FIELD[currentCounter + (FIELD_SIZE)].append(currentCounter) 
            currentCounter += 1
    return FIELD

def minimum(dict):
    min_key = list(dict.keys())[0]
    for i in list(dict.keys())[1:]:
        if dict[i] < dict[min_key]:
            min_key = i
    return(min_key)

def dijkstra(connections, start, end, all_vertexes, NUM_COLUMNS, FIELD_SIZE):
    routes = {}
    unexplored = all_vertexes
    unexplored[start] = 0
    while len(unexplored) != 0:
        explore = minimum(unexplored)
        if explore == end:
            routes[explore] = routes[explore]  + ", " + str(explore)
            break
        else:
            #make differnce between layers with a difference of the coefficient (useless = (layer - 1) * (FIELD_SIZE))
            #HERE: we go through every connection of the start vertex
            for index, value in enumerate(connections[explore]):    
                if value - explore == 1 or value - explore == -1 or value - explore == NUM_COLUMNS or value - explore == -NUM_COLUMNS:
                    #connection on same layer 
                    if value in unexplored.keys():
                        if unexplored[value] == sys.maxsize:
                            unexplored[value] = unexplored[explore] + 1
                        else:
                            check_time = unexplored[explore] + 1
                            #check if there is a shorter way
                            if check_time < unexplored[value]:
                                unexplored[value] = check_time
                        #saving a way to current vertex
                        if explore in routes.keys():
                            routes[value] = str(routes[explore]) + ", " + str(explore)
                        else:
                            routes[value] = str(explore)

                if value - explore == FIELD_SIZE or value - explore == -(FIELD_SIZE):
                    #connection to another layer
                    if value in unexplored.keys():
                        if unexplored[value] == sys.maxsize:
                            unexplored[value] = unexplored[explore] + 3
                        else:
                            check_time = unexplored[value] + 3
                            #check if there is a shorter way
                            if check_time < unexplored[value]:
                                unexplored[value] = check_time
                    #saving a way to current vertex
                    if explore in routes.keys():
                        routes[value] = str(routes[explore]) + ", " + str(explore) + "(telep)"
                    else:
                        routes[value] = str(explore) + "(telep)"

            del unexplored[explore]
        #remove node that was checked/explored
    return(unexplored[explore], routes)


#https://bwinf.de/fileadmin/bundeswettbewerb/42/BwInf_42_Aufgaben_WEB.pdf
#https://bwinf.de/bundeswettbewerb/42/1/

COORDINATES_A = []
COORDINATES_B = []
FILE_NAME = "field.txt"

#class node, fields: connections, coordinate
#class field of node, fields: nodes
#class route, fields: nodes(selected for current route)  
def main(): 
    start_time = time.time()
    #input in programm
    #y = n, x = m
    file_content = []
    read_first_line = []
    with open(r"/Users/tkr/Praktikum/" + FILE_NAME) as file:
        read_first_line = file.readline().split(" ")
        file_content = file.read().split("\n")

    NUM_ROWS, NUM_COLUMNS =  int(read_first_line[0]), int(read_first_line[1])
    FIELD_SIZE = NUM_ROWS * NUM_COLUMNS
    
    first_field_withSymbols = []
    second_field_withSymbols = []
    first_field_withSymbols, second_field_withSymbols = split_originall_field(file_content, NUM_ROWS)          
    
    FIELD = define_field(NUM_ROWS, NUM_COLUMNS, first_field_withSymbols, second_field_withSymbols)

    all_vertexes = {}
    #for 2 fields
    for i in range(NUM_COLUMNS, 2 * NUM_ROWS * NUM_COLUMNS):
        #all possible vertexes
        all_vertexes.setdefault(i, sys.maxsize)

    # minimum function for dictionary,
    # it will return the key who have the smallest value
    # 101 x 101 20.19 s   Elapsed time:  13.819849252700806
    # 201 x 81  45,86 s   Elapsed time:  34.96958565711975
    # 
    
    number_of_A = (NUM_COLUMNS * COORDINATES_A[1]) + COORDINATES_A[0]
    number_of_B = (NUM_COLUMNS * COORDINATES_B[1]) + COORDINATES_B[0]
    fastest_solution, routes = dijkstra(FIELD, number_of_A, number_of_B, all_vertexes, NUM_COLUMNS, FIELD_SIZE)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_the_results(number_of_A, number_of_B, elapsed_time, fastest_solution, routes[number_of_B])
    
main()
