# Penn Labs Backend Challenge

## Documentation

Relevant Files:
1. app.py - runs the Flask API 
   - Routes:
      - "/" -> API test (returns welcome string).
      - "/api" -> API JSON route test (returns welcome JSON).
      - "/api/clubs" -> responds to GET requests to return a JSON array of clubs.

2. db_create.py - creates SQLAlchemy database in a separate file to prevent circular imports where multiple instances of the database is created.

3. models.py - contains all the database models.

4. bootstrap.py - populates the database with club data and users.

4. clubs.json - legacy club JSON data.


Models: 
1. Club - represents a Penn Club in the database.
   - Attributes: 
      - code -> unique club code/abbreviation.
      - name -> club name.
      - description -> club description.
      - tags -> one-word club tags, in list format.
   - Methods:
      - to_dict -> convert a Club object to a JSON dict.
      - from_dict (static) -> convert a JSON dict to a Club object.
2. Tag - a particular club tag, connected to a Club model 
   - Attributes:
      - name -> tag name.
      - clubs -> the clubs that contain that tag.
   - Methods:
      - get_or_create (static) -> retrieve a tag or create a new one if that tag doesn't exist.
3. User - a user of Penn Club Review
   - Attributes:
      - username -> unique username to distinguish between users.
      - email -> email for communcation.
      - display_name -> name displayed on signups/membership lists (likely the user's real name for identification purposes).
      - admin -> does the user recieve Penn Club Review admin privelages? Useful for bugfixing or QA testing. 
      - created -> the date/time the account was created. Useful for account verificaiton. 
   - Methods:
      - to_dict -> convert a JSON dict to a User object.
      - from_dict (static) -> convert a User object to a JSON dict.


## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipx`
   - `brew install pipx` (macOS)
   - See instructions here https://github.com/pypa/pipx for other operating systems
4. Install `poetry`
   - `pipx install poetry`
5. Install packages using `poetry install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Activate the Poetry shell with `poetry shell`.
2. Run `python3 bootstrap.py` to create the database and populate it.
3. Use `flask run` to run the project.
4. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-862656cb8b7048db95aaa4e2935b77e5).
5. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `poetry add <package_name>` within the directory. Make sure to document your additions.
