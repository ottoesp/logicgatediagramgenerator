# Text-Base Logic Diagram Generator
## Overview
This is a tool for quickly and easily generating text based logic diagrams with minimal fuss. While this is largley a hobby project with many interesting algorithms behind it, some applications in edu-tech have limited support for images as inputs. Moreover, text-based diagrams are quite hard to make by hand (especially with non-standard characters) so a generator may be helpful.
This repo includes both the django website and diagram generating module.
### Features
* Automatically generates diagrams from logical phrases
* Control the maximum width (in gates/variables) of diagrams to fit your needs
## Get Started
### Running the server
To run the django server, cd into the root directory and run the following command
```
>> python manage.py runserver
```
### Diagram generator function
Under ```logicgatediagramgenerator/diagramGenerator/``` there is a main.py file. From this file, import the function ```generate_diagram(wff, w)``` which takes a string input of the logic statement and a maximum width of the diagram.
## About the algorithm
This is a hobby project so allow me to nerd out a bit. (TBC)
### Input parsing
### Layering algorithm
### Lane Assignment
### Rendering
## TODO
* Include more types of logic gates
  * XOR, NOR, XNOR (this one may be weird since it is >3 characters)
* Improve input validation
* Include indication of error handling
* Experiment with parameters of simulated annealing process
* Add selector on website for input width
* Add informative text instead of the Hobbit opening lines
* Add loading indicator while waiting for response (could allow for more SA steps)
* Add 1 or 2 'spare' lanes in lane allocation to give it some more wiggle room to avoid the dreaded #
* Fill out 'about the algorithm section'
