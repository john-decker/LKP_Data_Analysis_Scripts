#General Information
The script and data in this repository are part of an ongoing digital humanities project focused on the Sint Leonarduskerk in Zoutleeuw, Belgium. The outputs represent an initial foray into analyzing the data from a database that is currently under construction.

#Environment
The script in this file was developed using Anaconda (4.10.3) in Sublime with the Anaconda environment active. Failing to activate the environment will result in multiple errors. If Anaconda is not used, it will be necessary to ensure that Pandas and Matplotlib are installed.

#Inputs
The scripts rely on three .csv files and a .txt file -- item_refined.csv, person.csv, person_to_item.csv, and sorted_stops.txt. These files are available in the data folder. Please note that the csv files reflect the state of a database as of the date that this repository was posted. If and when future updates are made to these files, the outputs of the script will change to reflect the changed data. 

#Outputs
The script is designed to output four plots (these are available in the plots file) as well as a csv file titled "items_by_person. The script is currently configured so that the plots output but are not saved and the csv writer is currently commented out. To save the plots, and the txt file, simple uncomment the appropriate lines of code. 