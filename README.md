# Text-Base Logic Diagram Generator
## Overview
This is a tool for quickly and easily generating text based logic diagrams with minimal fuss. While this is largley a hobby project with many interesting algorithms behind it, some applications in edu-tech have limited support for images as inputs. Moreover, text-based diagrams are quite hard to make by hand (especially with non-standard characters) so a generator may be helpful.
This repo includes both the django website and diagram generating module.
### Features
* Automatically generates diagrams from logical phrases
* Control the maximum width (in gates/variables) of diagrams to fit your needs
## Get Started
### Using via the website
This tool is currently hosted at https://ottoesp.pythonanywhere.com/
### Running the server
To run the django server, cd into the root directory and run the following command
```
>> python manage.py runserver
```
### Diagram generator function
Run the file ```logicgatediagramgenerator/diagramGenerator/profiler.py "<Logical Sentence>"  <Maximum node width>``` modify this to supress profiler information 
## TODO
* Host
* **Add Copy Button**
