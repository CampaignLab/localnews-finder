# localnews-finder

Find local news relevant to a constituency

# Architecture

A Python server built with Chalice, meant to run on AWS Lambda. A React frontend built with Next.js, deployed to AWS S3 and served with CloudFront.

# Backend

## Running locally

You must have Python3 installed on a Unix-like system.

Then:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
chalice local --port 5000
```

This will create a server at http://127.0.0.1:5000

## Sending commands to the server

http://127.0.0.1:5000/constituencies will return a sorted list of constituencies.

`http://127.0.0.1:5000/search?constituency=<url-encoded constituency name>&topic=<searchTerm>` will return the news search results.

# Frontend

## Running locally

```bash
cd frontend
curl -fsSL https://bun.sh/install | bash
bun install
echo "NEXT_PUBLIC_BASE_URL=http://127.0.0.1:5000" > .env.local
bun dev
```

This will create a site at http://127.0.0.1:3000 that you can test with.

# Deploying

You must have a `~/.aws/config` file set up as follows:

```
[default]
aws_access_key_id=<our access key>
aws_secret_access_key=<our secret key>
region=eu-west-2
```

Log into the AWS console to get the values for these keys.

Please only deploy code that is merged to the `main` branch.

## Deploying the backend

```bash
cd backend
chalice deploy
```

## Deploying the frontend

From the frontend directory, run `bun run build` (not `bun build`). This will export HTML/JS files to a subdirectory `out`.

Use the AWS console to upload the contents of this directory to our S3 bucket. We don't yet have a script for this.

The site is currently running at https://d30wfp6i5v88nt.cloudfront.net/
