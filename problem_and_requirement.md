Problem and requirement analysis
DRAFT
- A markdown document together with flowchart

1. Simulate annual cycle of Herbivore without migration
- Define variables: age, weight to use in Fitness Function.
    - For weight we need a function returning Gaussian distributed
    numbers to find birthweight of the animals
    - Assume first amount of food is fixed F every year. Then
     assume animal is in a cell in Highland.
    - Define functions for birth and death
 
 2. After completion of working simulation of Herbivore, make a super class
 with common methods and attributes of both animals. Then continue with
 a subclass Carnivore implementing specific requirements for that class.
 
 3. Start with migration between the same cell type e.g Highland. Continue with 
 defining classes for different cell types. With a super class for common methods and
 attributes. 
  
 4. Make a coordinate system of the Island as a list of tuples? The outer edge is fixed
 as water. The remaining cells is random? Find a way to generate the Island with
 some fixed and some random cells.
 
 5. The Herbivores and Carnivores start from one cell and migrate from there. Their
 populations are given as lists of dictionaries.
 
 6. Plotting using matplotlib. Then visualize the corresponding PNG plots into a movie
  using FFMPEG. 
  
 7. Extras