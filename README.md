Project summary
-
My project implements a user non-relational database with dynamodb and a relational database, movies. The user table stores first names, last names, and birthdays. That information is used to pull results from the movie table. My project relates my users to movies in two ways. First, a user can select their first name from a drop down of all user first names and a table will be returned with all actors/actresses with the same name. The other functionality that combines the two tables is matching user birthdays to release dates. Again, the user selects their first name from a drop down list. Then, a table is returned with the movies that were released on the date listed as the birthday for that user.

Technologies used
-
I used Visual Studio Code and AWS for the majority of the project. I also used ChatGPT for troubleshooting.

Setup and run instructions
-
My code is split up into two files: flaskfile.py and sqlfunctions.py. flaskfile.py imports sqlfunctions.py, so flaskfile.py is the one I run to create the website. I kept flaskfile.py as long as it is because I wanted to keep all the functions for my pages on one file. I also have seven template files. One is for home, four are for CRUD, and two for my movie pages. 
