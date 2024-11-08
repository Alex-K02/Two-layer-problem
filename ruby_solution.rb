
fileName = "field.txt"

content = Array.new
File.open("/Users/tkr/Praktikum/" + fileName, 'r') do |file|
  # Read the entire file content
  size = file.readline().split(" ")
  NUM_OF_ROWS, NUM_OF_COLUMNS = size[0].to_i, size[1].to_i

  content = file.read().split("\n")
end

#constant value field size
FIELD_SIZE = NUM_OF_ROWS * NUM_OF_COLUMNS
first_field_withSymbols = []
second_field_withSymbols = []

i = 0
#separating two fields in two arrays
#then: in 1 loop cycle you can analyse certain rows of both fields
while i < (2 * NUM_OF_ROWS + 1)
  if content[i] != ""
    if i < NUM_OF_ROWS
      first_field_withSymbols.append(content[i])
    else
      second_field_withSymbols.append(content[i])
    end
  end
  i += 1
end

# initializing both fields
field = Array.new(2 * FIELD_SIZE) { [] }

allVertex = Hash.new
# creating a dictionary for all possible connections
i = NUM_OF_COLUMNS
while i < (2 * FIELD_SIZE)
  allVertex.store(i, Float::INFINITY)
  i += 1
end

coordinates_A = Array.new
coordinates_B = Array.new

#counter for all elements of the field
#it will count like that:
# 0 1 2 3 4 5
# # # # # # #
# 6 7 8 9 10 11
# # A # B  . #
currentCounter = 0
# here will be defined coordinates of A,B and connections between dots
for i in 0..(NUM_OF_ROWS - 1)
  for j in 0..(NUM_OF_COLUMNS - 1)

    #define coordinates of A
    if first_field_withSymbols[i].include?("A")
      if coordinates_A.empty?
        coordinates_A.append(first_field_withSymbols[i].index("A"))
        coordinates_A.append(i)
      end
    end
    #define coordinates of B
    if first_field_withSymbols[i].include?('B')
      if coordinates_B.empty?
        coordinates_B.append(first_field_withSymbols[i].index('B'))
        coordinates_B.append(i)
      end
    end

    #check if current position on first field is not a wall 
    if first_field_withSymbols[i][j] == '.' or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B'
      # left
      if first_field_withSymbols[i][j - 1] == '.' or first_field_withSymbols[i][j - 1] == 'A' or first_field_withSymbols[i][j - 1] == 'B'
        field[currentCounter].append(currentCounter - 1)
      end
      # right
      if j + 1 < first_field_withSymbols[i].length and (first_field_withSymbols[i][j + 1] == '.' or first_field_withSymbols[i][j + 1] == 'A' or first_field_withSymbols[i][j + 1] == 'B')
        field[currentCounter].append(currentCounter + 1)
      end
      # top
      if first_field_withSymbols[i - 1][j] == '.' or first_field_withSymbols[i - 1][j] == 'A' or first_field_withSymbols[i - 1][j] == 'B'
        ind = (NUM_OF_COLUMNS * (i - 1)) + j
        field[currentCounter].append(ind)
      end
      # bottom
      if first_field_withSymbols[i + 1][j] == '.' or first_field_withSymbols[i + 1][j] == 'A' or first_field_withSymbols[i + 1][j] == 'B'
        ind = (NUM_OF_COLUMNS * (i + 1)) + j
        field[currentCounter].append(ind)
      end

      # teleport
      if second_field_withSymbols[i][j] == '.'
        field[currentCounter].append(currentCounter + FIELD_SIZE)
      end
    end

    #check if same position on the second field is not a wall 
    #possible to teleport
    if second_field_withSymbols[i][j] == '.'
      #left
      if second_field_withSymbols[i][j - 1] == '.'
        field[currentCounter + FIELD_SIZE].append(currentCounter - 1 + FIELD_SIZE)
      end
      #right
      if j + 1 < second_field_withSymbols[i].length and second_field_withSymbols[i][j + 1] == '.'
        field[currentCounter + FIELD_SIZE].append(currentCounter + 1 + FIELD_SIZE)
      end
      #top
      if second_field_withSymbols[i - 1][j] == '.'
        ind = (NUM_OF_COLUMNS * (i - 1)) + j
        field[currentCounter + FIELD_SIZE].append(ind + FIELD_SIZE)
      end
      #bottom
      if i + 1 < second_field_withSymbols.length and second_field_withSymbols[i + 1][j] == '.'
        ind = (NUM_OF_COLUMNS * (i + 1)) + j
        field[currentCounter + FIELD_SIZE].append(ind + FIELD_SIZE)
      end
      #teleport
      if first_field_withSymbols[i][j] == '.' or first_field_withSymbols[i][j] == 'A' or first_field_withSymbols[i][j] == 'B'
        field[currentCounter + FIELD_SIZE].append(currentCounter)
      end
    end
    currentCounter += 1
  end
end

routes = Hash.new

#searching for the dot with smallest distance
def minimum(dict)
  min_key = dict.keys[0]
  dict.keys[1..].each do |i|
    if dict[i] < dict[min_key]
      min_key = i
    end
  end
  min_key
end


def dijkstra(connections, startCoordinate, endCoordinate, allVertex)
  allVertex[startCoordinate] = 0
  while allVertex.keys.any?
    #finding the position with the smallest distance
    explore = minimum(allVertex)
    #checking if its coordinate same as coordinate of B
    if explore == endCoordinate
      break
    end
    #HERE: we go through every connection of the start vertex
    connections[explore].each { |index|
      if allVertex.include?(index)
        if allVertex.key?(index)
          #define teleport index (for a dot on 1 field it will be on second, and for the dot on the second will be on first)
          teleport_index = explore >= FIELD_SIZE ? explore - (FIELD_SIZE) : explore + (FIELD_SIZE)
          #conditions when current position and dot we are looking at, are on the same field
          if (index <= FIELD_SIZE && explore <= FIELD_SIZE) || (index >= FIELD_SIZE && explore >= FIELD_SIZE)
            if allVertex[index] == Float::INFINITY
              allVertex[index] = allVertex[explore] + 1
            else
              check_time = allVertex[explore] + 1
              allVertex[index] = check_time if check_time < allVertex[index]
            end
          end
          #conditions whan current position and dot are on different fields
          if (index <= FIELD_SIZE && explore >= FIELD_SIZE) || (index >= FIELD_SIZE && explore <= FIELD_SIZE)
            if allVertex.key?(index)
              if allVertex[index] == Float::INFINITY
                allVertex[index] = allVertex[explore] + 3
              else
                check_time = allVertex[index] + 3
                allVertex[index] = check_time if check_time < allVertex[index]
              end
            end
          end
        end
      end
    }
    allVertex.delete(explore)
  end
  allVertex[explore]
end

#calculating index of A and B
indexOfA = (NUM_OF_COLUMNS * coordinates_A[1]) + coordinates_A[0]
indexOfB = (NUM_OF_COLUMNS * coordinates_B[1]) + coordinates_B[0]

fastestSolution = dijkstra(field, indexOfA, indexOfB, allVertex)
puts "Fastest solution = #{fastestSolution.inspect}"
