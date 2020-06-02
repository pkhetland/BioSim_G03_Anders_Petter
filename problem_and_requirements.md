# Problem and requirement analysis
*A markdown document providing an overview of the coding project together with 
a flowchart (filename)*

### 1. Implement `Herbivore class` and `Highland class`
- Create a minimum viable implementation of two classes to 
prepare for step 2.
- Start by writing tests for both classes, then writing the classes.
- *For `Herbivore`*: 
    - Define variables: `age`, `weight` to use in `Fitness Function`.
    - For `weight` we need a function returning Gaussian distributed
    numbers to find `birth weight` of the animals
- *For `Highland`*: 
    - Define variables: `food`, `food_max`

### 2. Simulate annual cycle of `Herbivore` without migration
- Assume first amount of food is fixed F every year. Then
 assume animal is in a cell in Highland.
- Implement `annual_cycle`:
    - Define methods for `birth` and `death`
    - Define methods for `mating` and `feeding`

### 3. Create `Animal class` and implement `Carnivore class`
After completion of working simulation of Herbivore, make a super class
with common methods and attributes of both animals. Then continue with
a subclass Carnivore implementing specific requirements for that class.

### 4. Simulate annual cycle of both animals in migration between two `Highland` cells

### 5. Implement `Lowland class` and simulate migration between two cells of different terrain
Start with migration between the same cell type e.g Highland. Continue with 
defining classes for different cell types. With a super class for common methods and
attributes. 

### 6. Create a semi-random coordinate system 
Make a coordinate system of the Island as a list of tuples? The outer edge is fixed
as water. The remaining cells is random? Find a way to generate the Island with
some fixed and some random cells.

### 7. Create a simulation with animals starting in one cell and full migration
The Herbivores and Carnivores start from one cell and migrate from there. Their
populations are given as lists of dictionaries.

### 8.  Plotting using matplotlib
Then visualize the corresponding PNG plots into a movie using FFMPEG. 

### 9. Further improvements...