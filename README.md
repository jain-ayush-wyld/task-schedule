# task-schedule
make sure to install these libraries
pip install fastapi uvicorn python-multipart jinja2

To make the hosting live use below command in cmd prompt
python -m uvicorn main:app --reload

you will see link of port on which python app is live follow the link

1.  How exactly did you use AI while building this? List tools, prompts, successes, and 
failures.
designing the front end part, and getting the routes created in python using fastapi, in logic part of script.js had to dry run, test modify acc.,
also in routes logic much part was needed to hard code out

3.  If given two more days, what would you refactor or add first, and why?
I will refractor the slots showing endpoint as once book is clicked the new slots are not updated in the list and can lead to clashes and errors.
Then try to sort the calender and show to user, increaces readibility.
so connect to a database as currently information wipes out once site is reloaded.
