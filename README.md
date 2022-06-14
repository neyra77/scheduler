# scheduler
Problem: Let's say a student wants to take 4 courses this semester, some classes may have 10 different sections out of which a student has to pick one to enroll. 
  It was truly a pain to create a decent schedule by hand where the hours were not all over the place (since students here don't live in dorms, a schedule where
  classes followed one after another to minimize school commute was best) without spending many many hours.
  
Solution: Given the HTML file where the schedules are posted, this program creates a visual representation of all possible schedules that a student can choose 
  from with the courses they want to take this semester. With a quick visual scan, they can choose a schedule that looks good and examine it as these are saved as 
  image files. They can then proceed to enroll since the schedule is written there. 





Once the university-given list of classes is saved as an HTML file to the /files directory, the program can be run with the following command

  python3 scheduler.py -H [schedule HTML file] -J [JSON file in /JSON directory which if doesn't exist will create it]

The program then does the following
1. Scrape the HTML file (using Beautiful Soup)
2. Organizes and stores the Course details into Course Objects (see course.py)
  a. Also makes a JSON representation of it to store into the file named with the -J flag
     The reason for this is that next time we won't have to scrape the HTML again but can just read the course info from the JSON file. 
3. Requests the user to input the classes they want this semester. 
4. Creates schedules (in text) and stores them into ./result directory. 
5. We then can run the command 'python3 plot.py' which uses the text schedules from the ./results directory and stores the schedule images into a ./images directory
