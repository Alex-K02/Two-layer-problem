#Dijkstra solution
import sys, time


def print_the_results(number_of_A, number_of_B, elapsed_time, fastest_solution, final_route):
    print("The smallest time needed from A(" + str(number_of_A) + ") to B(" + str(number_of_B) + ") = " + str(fastest_solution))
    print("Route form A to B: " + str(final_route))
    print("Elapsed time: ", elapsed_time)


def split_originall_field(file_content, num_rows):
    first_field_withSymbols = []
    second_field_withSymbols = []
    for i in range(0, 2 * num_rows + 1):
        if file_content[i] == "":
            continue
        if i < num_rows:
            first_field_withSymbols.append(file_content[i])
        else:
            second_field_withSymbols.append(file_content[i])
    return first_field_withSymbols, second_field_withSymbols


def define_connections(num_rows, num_columns, first_field_withSymbols, second_field_withSymbols):
    field_size = num_rows * num_columns
    connections = [[] for i in range(0, 2 * field_size)]
    global_field_index = 0
    for row_index in range(0, num_rows):
        #for both fields
        if first_field_withSymbols[row_index].find('A') != -1 or second_field_withSymbols[row_index].find('A') != -1:
                if not coordinates_A:
                    if first_field_withSymbols[row_index].find('A') != -1:
                        coordinates_A.append(first_field_withSymbols[row_index].find('A'))
                        coordinates_A.append(row_index)
                    else:
                        coordinates_A.append(second_field_withSymbols[row_index].find('A'))
                        coordinates_A.append(row_index + num_rows)
        if first_field_withSymbols[row_index].find('B') != -1 or second_field_withSymbols[row_index].find('B') != -1:
            if not coordinates_B:
                if first_field_withSymbols[row_index].find('B') != -1:
                    coordinates_B.append(first_field_withSymbols[row_index].find('B'))
                    coordinates_B.append(row_index)
                else: 
                    coordinates_B.append(second_field_withSymbols[row_index].find('B'))
                    coordinates_B.append(row_index + num_rows)

        for column_index in range(0, num_columns):
            if first_field_withSymbols[row_index][column_index] == '.' or first_field_withSymbols[row_index][column_index] == 'A' or first_field_withSymbols[row_index][column_index] == 'B':
                #left
                if first_field_withSymbols[row_index][column_index - 1] == '.' or first_field_withSymbols[row_index][column_index - 1] == 'A' or first_field_withSymbols[row_index][column_index - 1] == 'B':
                    #ind = global_field_index - 1
                    connections[global_field_index].append(global_field_index - 1)
                #right
                if column_index + 1 < len(first_field_withSymbols[row_index]) and (first_field_withSymbols[row_index][column_index + 1] == '.' or first_field_withSymbols[row_index][column_index + 1] == 'A' or first_field_withSymbols[row_index][column_index + 1] == 'B'):
                    #ind = global_field_index + 1
                    connections[global_field_index].append(global_field_index + 1)
                
                #top
                if first_field_withSymbols[row_index - 1][column_index] == '.' or first_field_withSymbols[row_index - 1][column_index] == 'A' or first_field_withSymbols[row_index - 1][column_index] == 'B':
                    ind = (num_columns * (row_index - 1)) + column_index
                    connections[global_field_index].append(ind) 
                
                #bottom
                if first_field_withSymbols[row_index + 1][column_index] == '.' or first_field_withSymbols[row_index + 1][column_index] == 'A' or first_field_withSymbols[row_index + 1][column_index] == 'B':
                    ind = (num_columns * (row_index + 1)) + column_index
                    connections[global_field_index].append(ind) 
                    
                #teleport
                if second_field_withSymbols[row_index][column_index] == '.':
                    connections[global_field_index].append(global_field_index + (field_size)) 
            #for second field
            if second_field_withSymbols[row_index][column_index] == '.' or second_field_withSymbols[row_index][column_index] == 'A' or second_field_withSymbols[row_index][column_index] == 'B':
                #left
                if second_field_withSymbols[row_index][column_index - 1] == '.' or second_field_withSymbols[row_index][column_index - 1] == 'A' or second_field_withSymbols[row_index][column_index-1] == 'B':
                    connections[global_field_index + (field_size)].append(global_field_index - 1 + (field_size))
                
                #right
                if column_index + 1 < len(second_field_withSymbols[row_index]) and second_field_withSymbols[row_index][column_index + 1] == '.' or second_field_withSymbols[row_index][column_index + 1] == 'A' or second_field_withSymbols[row_index][column_index + 1] == 'B':
                    connections[global_field_index + (field_size)].append(global_field_index + 1 + (field_size))
                
                #top
                if second_field_withSymbols[row_index - 1][column_index] == '.' or second_field_withSymbols[row_index - 1][column_index] == 'A' or second_field_withSymbols[row_index - 1][column_index] == 'B':
                    ind = (num_columns * (row_index - 1)) + column_index
                    connections[global_field_index + (field_size)].append(ind + (field_size))
                
                #bottom
                if row_index + 1 < len(second_field_withSymbols) and second_field_withSymbols[row_index + 1][column_index] == '.' or second_field_withSymbols[row_index + 1][column_index] == 'A' or second_field_withSymbols[row_index + 1][column_index] == 'B':
                    ind = (num_columns * (row_index + 1)) + column_index 
                    connections[global_field_index + (field_size)].append(ind + (field_size))
                    
                #teleport
                if first_field_withSymbols[row_index][column_index] == '.' or first_field_withSymbols[row_index][column_index] == 'A' or first_field_withSymbols[row_index][column_index] == 'B':
                    connections[global_field_index + (field_size)].append(global_field_index) 
            global_field_index += 1
    return connections

# minimum function for dictionary,
# it will return the key who have the smallest value
def minimum(dict):
    min_key = list(dict.keys())[0]
    for i in list(dict.keys())[1:]:
        if dict[i] < dict[min_key]:
            min_key = i
    return(min_key)


def dijkstra(connections, start, end, all_vertexes, num_columns, field_size):
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
                if value - explore == 1 or value - explore == -1 or value - explore == num_columns or value - explore == -num_columns:
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

                if value - explore == field_size or value - explore == -(field_size):
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
    return(unexplored[explore], routes[end])

#ASSIGNMENT
#https://bwinf.de/fileadmin/bundeswettbewerb/42/BwInf_42_Aufgaben_WEB.pdf
#https://bwinf.de/bundeswettbewerb/42/1/


coordinates_A = []
coordinates_B = []
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
    
    first_field_withSymbols = []
    second_field_withSymbols = []
    first_field_withSymbols, second_field_withSymbols = split_originall_field(file_content, NUM_ROWS)          
    
    connections = define_connections(NUM_ROWS, NUM_COLUMNS, first_field_withSymbols, second_field_withSymbols)

    all_vertexes = {}
    #for both fields
    for i in range(NUM_COLUMNS, 2 * NUM_ROWS * NUM_COLUMNS):
        #all possible vertexes
        all_vertexes.setdefault(i, sys.maxsize)

    index_of_A = (NUM_COLUMNS * coordinates_A[1]) + coordinates_A[0]
    index_of_B = (NUM_COLUMNS * coordinates_B[1]) + coordinates_B[0]
    fastest_solution, route = dijkstra(connections, index_of_A, index_of_B, all_vertexes, NUM_COLUMNS, NUM_ROWS * NUM_COLUMNS)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print_the_results(index_of_A, index_of_B, elapsed_time, fastest_solution, route)
    
main()
