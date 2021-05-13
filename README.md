# Grafy_2021

##How to start:

To install all depedencies used by the project run:

```pip3 install -r requirements.txt```

To start the app in interactive mode run the main file without any additional parameters. Use the following command:

 ```python3 src/main.py```
 
 If you want to use the app in command line mode, specify tasks you want to execute. You can find all the available options by running the app with -h or --help parameter e.g.:
 
  ```python3 src/main.py -h```
  
  Few hints
  
 1. You have to specify required --generate-np argument.
 2. You can (or rather you must) specify multiple arguments in one line e.g.:
 ```python3 src/main.py --generate-np10 0.4 --draw --center-minimax --save out.txt 2```
 3. Order of the arguments does not matter. All specified arguments will run only once, always in the same order.


Input files have to be stored in the data folder.
 
 ####Contributors:
 
 - [Gabriela Leśniak](https://github.com/gabi15) 
 - [Adrianna Leśna](https://github.com/atrria)
 - [Aleksandra Kuś](https://github.com/awku)
 - [Paweł Korytowski](https://github.com/pkorytowski)