#Dijkstra solution
import sys, time
fileName = "yourFileName.txt"

#https://bwinf.de/fileadmin/bundeswettbewerb/42/BwInf_42_Aufgaben_WEB.pdf
#https://bwinf.de/bundeswettbewerb/42/1/

def main():
    start_time = time.time()
    #input in programm
    #y = n, x = m
    file = open(r"/your/path" + fileName)
    size = file.readline().split(" ")
    n, m =  int(size[0]), int(size[1])
    content = file.read().split("\n")
    file.close()
    first_field_withSymbols = []
    second_field_withSymbols = []
    for i in range(0, 2*n + 1):
        if content[i] == "":
            continue
        if i < n:
            first_field_withSymbols.append(content[i])
        else:
            second_field_withSymbols.append(content[i])            

    field = [[0] * (n * m + 1) for i in range(0, 2 * n * m)]

    allVertexes = {}
    #for 2 fields
    for i in range(m, 2 * n * m):
        #all possible vertex without teleport
        #TODO: make one hash table for all fields 
        allVertexes.setdefault(i, sys.maxsize)

    coordinates_A = []
    coordinates_B = []

    currentCounter = 0
    for i in range(0, n - 1):
        for j in range(0, m):

            if first_field_withSymbols[i].find('A') != -1:
                if not coordinates_A:
                    coordinates_A.append(first_field_withSymbols[i].find('A'))
                    coordinates_A.append(i)
            if coordinates_B == 0 or first_field_withSymbols[i].find('B') != -1:
                if not coordinates_B:
                    coordinates_B.append(first_field_withSymbols[i].find('B'))
                    coordinates_B.append(i)
            
            if first_field_withSymbols[i][j] == '.' or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B':
                #left
                if first_field_withSymbols[i][j - 1] == '.' or first_field_withSymbols[i][j - 1] == 'A' or first_field_withSymbols[i][j - 1] == 'B':
                    #ind = currentCounter - 1
                    field[currentCounter][currentCounter - 1] = 1 
                #right
                if j + 1 < len(first_field_withSymbols[i]) and (first_field_withSymbols[i][j + 1] == '.' or first_field_withSymbols[i][j + 1] == 'A' or first_field_withSymbols[i][j + 1] == 'B'):
                    #ind = currentCounter + 1
                    field[currentCounter][currentCounter + 1] = 1 
                
                #top
                if first_field_withSymbols[i - 1][j] == '.' or first_field_withSymbols[i - 1][j] == 'A' or first_field_withSymbols[i - 1][j] == 'B':
                    ind = (m * (i - 1)) + j
                    field[currentCounter][ind] = 1 
                
                #bottom
                if first_field_withSymbols[i + 1][j] == '.' or first_field_withSymbols[i + 1][j] == 'A' or first_field_withSymbols[i + 1][j] == 'B':
                    ind = (m * (i + 1)) + j
                    field[currentCounter][ind] = 1 
                    
                #teleport
                if second_field_withSymbols[i][j] == '.':
                    field[currentCounter][-1] = 3 

            
            #for second field
            if second_field_withSymbols[i][j] == '.':
                #left
                if second_field_withSymbols[i][j - 1] == '.':
                    field[currentCounter + (n * m)][currentCounter - 1] = 1
                
                #right
                if j + 1 < len(second_field_withSymbols[i]) and second_field_withSymbols[i][j + 1] == '.':
                    # a = currentCounter + (n * m) + 1
                    field[currentCounter + (n * m)][currentCounter + 1] = 1 
                
                #top
                if second_field_withSymbols[i - 1][j] == '.':
                    ind = (m * (i - 1)) + j
                    field[currentCounter + (n * m)][ind] = 1 
                
                #bottom
                if i + 1 < len(second_field_withSymbols) and second_field_withSymbols[i + 1][j] == '.':
                    ind = (m * (i + 1)) + j
                    field[currentCounter + (n * m)][ind] = 1 
                    
                # #teleport
                if field[currentCounter][-1] == 3 or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B':
                    field[currentCounter + (n * m)][-1] = 3 
            currentCounter += 1
            
    routes = {}
    
    def minimum(dict):
        min_key = list(dict.keys())[0]
        for i in list(dict.keys())[1:]:
            if dict[i] < dict[min_key]:
                min_key = i
        return(min_key)

    def dijkstra(connections, start, end):
        unexplored = allVertexes
        unexplored[start] = 0
        while len(unexplored) != 0:
            explore = minimum(unexplored)
            if explore == end:
                routes[explore] = routes[explore]  + ", " + str(explore)
                break
            else:
                #make differnce between layers with a difference of the coefficient (useless = (layer - 1) * (n * m))
                #HERE: we go through every connection of the start vertex
                for index in range(m, len(connections[start])):
                    #for 2 layer teleport coordinates: explore - (n * m),
                    #for 1 layer teleport coordinates: explore + (n * m)
                    teleportIndex = explore - (n * m) if explore >= n * m else explore + (n * m)
                    #check fields that are on the same layer
                    #for 2 = index + (n * m)
                    #for 1 = index
                    if explore >= n * m:
                        moveIndex = index + (n * m)
                    else: 
                        moveIndex = index

                    if connections[explore][index] == 1:
                        if moveIndex in unexplored.keys():
                            if unexplored[moveIndex] == sys.maxsize:
                                unexplored[moveIndex] = unexplored[explore] + connections[explore][index]
                                if explore in routes.keys():
                                    routes[moveIndex] = str(routes[explore]) + ", " + str(explore)
                                else:
                                    routes[moveIndex] = str(explore)
                            else:
                                check_time = unexplored[explore] + connections[explore][index]
                                if check_time < unexplored[moveIndex]:
                                    unexplored[moveIndex] = check_time
                                
                                if explore in routes.keys():
                                    routes[moveIndex] = str(routes[explore]) + ", " + str(explore)
                                else:
                                    routes[moveIndex] = str(explore)
                                    
                    if connections[explore][index] == 3:
                        if teleportIndex in unexplored.keys():
                            if unexplored[teleportIndex] == sys.maxsize:
                                unexplored[teleportIndex] = unexplored[explore] + connections[explore][index]
                                if explore in routes.keys():
                                    routes[teleportIndex] = str(routes[explore]) + ", " + str(explore) + "(telep)"
                                else:
                                    routes[teleportIndex] = str(explore) + "(telep)"
                            else:
                                check_time = unexplored[teleportIndex] + connections[explore][teleportIndex]
                                if check_time < unexplored[teleportIndex]:
                                    unexplored[teleportIndex] = check_time
                                
                                if explore in routes.keys():
                                    routes[teleportIndex] = str(routes[explore]) + ", " + str(explore) + "(telep)"
                                else:
                                    routes[teleportIndex] =  str(explore) + "(telep)"
                del unexplored[explore]
        #remove node that was checked/explored
        return(unexplored[explore])
    
    numberOfA = (m * coordinates_A[1]) + coordinates_A[0]
    numberOfB = (m * coordinates_B[1]) + coordinates_B[0] 
    fastest_solution = dijkstra(field, numberOfA, numberOfB)
    end_time = time.time()
    print("The smallest time needed from A(" + str((m * coordinates_A[1]) + coordinates_A[0]) + ") to B(" + str((m * coordinates_B[1]) + coordinates_B[0]) + ") = " + str(fastest_solution))
    print("route: " + str(routes[numberOfB]))
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    
main()
