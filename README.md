# localnews-finder

Find local news relevant to a constituency

# Running the server

You must have Python3 installed on a Unix-like system. Recommended to use virtualenv: `python -m venv .venv`

Then:

```python
source .venv/bin/activate
python app.py
```

This will create a server at http://localhost:5000

# Sending commands to the server

http://localhost:5000/constituencies will return a sorted list of constituencies.

http://localhost:5000/search?constituency=<url-encoded constituency name>&topic=<searchTerm>
