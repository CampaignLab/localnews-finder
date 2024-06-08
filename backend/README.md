# localnews-finder

Find local news relevant to a constituency

# Running the server

You must have Python3 installed on a Unix-like system.

Then:

```python
source .venv/bin/activate
pip install -r requirements.txt
chalice local --port 5000
```

This will create a server at http://127.0.0.1:5000

# Sending commands to the server

http://127.0.0.1:5000/constituencies will return a sorted list of constituencies.

`http://127.0.0.1:5000/search?constituency=<url-encoded constituency name>&topic=<searchTerm>` will return the news search results.
