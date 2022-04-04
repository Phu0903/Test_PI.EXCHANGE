# Solution:
- Data is read from the file template and the file data user using lib JSON and lib CVS
- With data file with divide 2 list. The list containing headers file's CVS and 1 list containing data user
- Get the body of the template and for loop data user. And then change the element required in the case study. If don't have email, write to file /path/to/errors.csv
else export output
# Test
- pip install unitest
- and run cmd "python -m unittest send_email.TestFirst"
# Run: 
  # Case 1: If have "python": 
- Run cmd "python .\send_email.py"
  # Case 2: If don't have "python" and on "Windows"
- Open folder "dist"
- Run cmd "send_email.exe"

