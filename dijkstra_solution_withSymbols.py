#Dijkstra solution
import sys, shutil, numpy
fileName = "yourFileName"
fileRoute = r"/your/path"

def main():
    #input in programm
    #y = n, x = m
    file = open(r"/your/path" + fileName + ".txt")
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
            
    # print(first_field_withSymbols)

    field = [[] for i in range(0, 2 * n * m)]

    # second_field = [[0] * (n * m + 1) for i in range(0, n * m)]
    allVertexes = {}
    #for 2 fields
    for i in range(0, 2 * n * m):
        #all possible vertex without teleport
        #TODO: make one hash table for all fields 
        allVertexes.setdefault(i, sys.maxsize)


    # visited = [False] * (n * m + 1)
    # layer = 1
    coordinates_A = []
    coordinates_B = []

    currentCounter = 0
    for i in range(0, n):
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
                    field[currentCounter].append(currentCounter - 1)
                #right
                if j + 1 < len(first_field_withSymbols[i]) and (first_field_withSymbols[i][j + 1] == '.' or first_field_withSymbols[i][j + 1] == 'A' or first_field_withSymbols[i][j + 1] == 'B'):
                    #ind = currentCounter + 1
                    field[currentCounter].append(currentCounter + 1)
                
                #top
                if first_field_withSymbols[i - 1][j] == '.' or first_field_withSymbols[i - 1][j] == 'A' or first_field_withSymbols[i - 1][j] == 'B':
                    ind = (m * (i - 1)) + j
                    field[currentCounter].append(ind)
                
                #bottom
                if first_field_withSymbols[i + 1][j] == '.' or first_field_withSymbols[i + 1][j] == 'A' or first_field_withSymbols[i + 1][j] == 'B':
                    ind = (m * (i + 1)) + j
                    field[currentCounter].append(ind)
                    
                #teleport
                if second_field_withSymbols[i][j] == '.':
                    field[currentCounter].append(currentCounter + n * m)

            
            #for second field
            if second_field_withSymbols[i][j] == '.':
                #left
                if second_field_withSymbols[i][j - 1] == '.':
                    field[currentCounter + (n * m)].append(currentCounter + (n * m) - 1)
                
                #right
                if j + 1 < len(second_field_withSymbols[i]) and second_field_withSymbols[i][j + 1] == '.':
                    # a = currentCounter + (n * m) + 1
                    field[currentCounter + (n * m)].append(currentCounter + (n * m) + 1)
                
                #top
                if second_field_withSymbols[i - 1][j] == '.':
                    ind = (m * (i - 1)) + j
                    field[currentCounter + (n * m)].append(ind + (n * m))
                
                #bottom
                if i + 1 < len(second_field_withSymbols) and second_field_withSymbols[i + 1][j] == '.':
                    ind = (m * (i + 1)) + j
                    field[currentCounter + (n * m)].append(ind + (n * m))
                    
                #possibly is 
                # #teleport field[currentCounter][-1] < (n * m)
                if field[currentCounter]:
                    if first_field_withSymbols[i][j] or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B':
                        field[currentCounter + (n * m)].append(currentCounter)
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
                routes[explore] = routes[explore]  + "," + str(explore)
                break
            else:
                #make differnce between layers with a difference of the coefficient (useless = (layer - 1) * (n * m))
                #HERE: we go through every connection of the start vertex
                if connections[explore]:
                    for indexInLoop, connectionIndex  in enumerate(connections[explore]):
                        if connectionIndex in unexplored:
                            #for 2 layer teleport coordinates: explore - (n * m),
                            #for 1 layer teleport coordinates: explore + (n * m)
                            teleportIndex = explore - (n * m) if explore >= n * m else explore + (n * m)
                            #check fields that are on the same layer
                            #for 2 = index + (n * m)
                            #for 1 = index

                            if (connectionIndex <= n * m and explore <= n * m) or (connectionIndex >= n * m and explore >= n * m):
                                if connectionIndex in unexplored.keys():
                                    if unexplored[connectionIndex] == sys.maxsize:
                                        unexplored[connectionIndex] = unexplored[explore] + 1
                                        #add node to the dict
                                        if explore in routes.keys():
                                            routes[connectionIndex] = str(routes[explore]) + "," + str(explore)
                                        else:
                                            routes[connectionIndex] = str(explore)
                                    else:
                                        check_time = unexplored[explore] + 1
                                        if check_time < unexplored[connectionIndex]:
                                            unexplored[connectionIndex] = check_time
                                        #add node to the dict
                                        if explore in routes.keys():
                                            routes[connectionIndex] = str(routes[explore]) + "," + str(explore)
                                        else:
                                            routes[connectionIndex] = str(explore)
                                            
                            if (connectionIndex <= n * m and explore >= n * m) or (connectionIndex >= n * m and explore <= n * m):
                                if teleportIndex in unexplored.keys():
                                    if unexplored[teleportIndex] == sys.maxsize:
                                        unexplored[teleportIndex] = unexplored[explore] + 3
                                        #add node to the dict
                                        if explore in routes.keys():
                                            routes[teleportIndex] = str(routes[explore]) + "," + str(explore)
                                        else:
                                            routes[teleportIndex] = str(explore)
                                    else:
                                        check_time = unexplored[teleportIndex] + 3
                                        if check_time < unexplored[teleportIndex]:
                                            unexplored[teleportIndex] = check_time
                                        #add node to the dict
                                        if explore in routes.keys():
                                            routes[teleportIndex] = str(routes[explore]) + "," + str(explore)
                                        else:
                                            routes[teleportIndex] =  str(explore)
                    del unexplored[explore]
        #remove node that was checked/explored
        return(unexplored[explore])
    
    def illustrationsOfTheRoute(route, fileText, fileName, fileRoute):
        route = route.split(",")
        shutil.copy(fileRoute + fileName + ".txt", fileRoute + fileName + "_route" + ".txt")
        for vertexIndex, vertexValue in enumerate(route):
            #check if current element is .
            y = int(int(vertexValue) / m) if int(vertexValue) < n*m else int(int(vertexValue) / m) + 1
            x = int(int(vertexValue) % m)
            if (fileText[y][x] == "." or fileText[y][x] == "B" or fileText[y][x] == "A") and vertexIndex + 1 < len(route):
                #check postition of the next elementroute[vertexIndex + 1] - route[vertexIndex]
                index = int(vertexIndex + 1)
                if int(route[index]) - int(route[index - 1]) == 1:
                    fileText[y] = fileText[y][:x] + '>' + fileText[y][x+1:]
                elif int(route[vertexIndex + 1]) - int(route[vertexIndex]) == -1:
                    fileText[y] = fileText[y][:x] + '<' + fileText[y][x+1:]
                elif int(route[vertexIndex + 1]) - int(route[vertexIndex]) == m:
                    fileText[y] = fileText[y][:x] + 'v' + fileText[y][x+1:]
                elif int(route[vertexIndex + 1]) - int(route[vertexIndex]) == -m: 
                    fileText[y] = fileText[y][:x] + '^' + fileText[y][x+1:]
                elif int(route[vertexIndex + 1]) - int(route[vertexIndex]) == m * n:
                    fileText[y] = fileText[y][:x] + '!' + fileText[y][x+1:]
                elif int(route[vertexIndex + 1]) - int(route[vertexIndex]) ==  -m * n:
                    fileText[y] = fileText[y][:x] + '!' + fileText[y][x+1:]
        
        with open(r"C:/Users/Alex/Downloads/" + fileName + "_route" + ".txt", mode="w") as file:
            for line in fileText:
                file.write(line + "\n")
    
    numberOfA = (m * coordinates_A[1]) + coordinates_A[0]
    numberOfB = (m * coordinates_B[1]) + coordinates_B[0]
    fastest_solution = dijkstra(field, numberOfA, numberOfB)
    end_time = time.time()
    print("The smallest time needed from A(" + str(numberOfA) + ") to B(" + str(numberOfB) + ") = " + str(fastest_solution))
    print("route: " + str(routes[numberOfB]))
    illustrationsOfTheRoute(routes[numberOfB], content, fileName, fileRoute)
main()
