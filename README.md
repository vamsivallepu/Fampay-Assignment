# Youtube Video API
This project allows you to fetch the latest videos from a YouTube channel and store them in a database. It also provides a dashboard to view the stored videos with filters and sorting options.

To get started with this project, follow these steps:

## Prerequisites
Install the required dependencies using 

`pip install -r requirements.txt`

## Installing and Setup
1. Clone this repository

`git clone https://github.com/vamsivallepu/Fampay-Assignment.git`

2. Install required packeges metioned in prerequisites

3. You can place your api_key in settings.py file

4. Setup Database

`python manage.py makemigrations`

`python manage.py migrate`

4. Open the command prompt and run the following cmd:

`python manage.py fetch_latest_videos`

By running the above cmd, it calls the youtube api for every 10 seconds and stores the new videos into the database. 

5. Run the server (in new command prompt):

`python manage.py runserver`

This will start the Django development server.

## Usage

There are two important pages in this project:

1. /api/videos - This page shows 9 out of all the stored videos in the database. You can navigate to other pages from the links provided bottom. All these results are latest videos sorted in reverse chronological order of their publishing date-time. 
2. /api/dashboard - This page is similar to /api/videos page along with accessibility to filter the results and sort them based on title and published time. 

- ***If quota exisits for one api_key, it automatically makes use of other keys available.***

- ***Made a dashboard to view the stored videos with filters and sorting options.***
