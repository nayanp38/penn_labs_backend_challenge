# Penn Labs Backend Challenge

## Documentation

Relevant Files:
1. app.py - runs the Flask API 
   - Routes:
      - "/" -> API test (returns welcome string).
      - "/api" -> API JSON route test (returns welcome JSON).
      - [GET] "/api/clubs" -> returns a JSON array of clubs.
      - [GET] "/api/users -> finds a user profile based on their username. Doesn't return the user id or email privacy reasons. Parameters:
         -  username 
      - [GET] "/api/clubs/search" -> returns all clubs whose name contains a queried substring. Parameters:
         - string 
      - [POST] "/api/clubs/create" -> creates a club and adds it to the database to be seen by future "/api/clubs" calls. Parameters:
         - code 
         - name 
         - description (optional)
         - tags (optional)
      - [POST] "api/clubs/favorite" -> favorites a club under a particular user. Parameters:
         - code 
         - username 
      - [PATCH] "/api/clubs/\<code\>" -> updates a club, but only works for admin users. The name, description, and tags of a club can be updated. The id and code of a club can't be updated since they are integral attributes of the club identity. Parameters:
         - \<code\> (in http:// request to separate the existing club code with the new club data)
         - username
         - name (optional)
         - description (optional)
         - tags (optional)
      - [GET] "/api/tags" -> returns a JSON list of all tags and the number of clubs that are tagged with each particular tag.


2. db_create.py - creates SQLAlchemy database in a separate file to prevent circular imports where multiple instances of the database is created.

3. utilities.py - contains utilities for other files to import (for organizational purposes).
   - Functions:
      - create_user -> creates a User object based on inputted attributes. 
      - create_club -> creates a Club attribute based on inputted attributes. 

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
      - from_dict (static) -> convert a JSON dict to a Club object. Static because the Club instance doesn't exist yet. 
2. Tag - a particular club tag, connected to a Club model 
   - Attributes:
      - name -> tag name.
      - clubs -> the clubs that contain that tag.
   - Methods:
      - get_or_create (static) -> retrieve a tag or create a new one if that tag doesn't exist. Static because it doesn't rely on a tag instance to operate (simply a utility function).
3. User - a user of Penn Club Review
   - Attributes:
      - username -> unique username to distinguish between users.
      - email -> email for communcation.
      - display_name -> name displayed on signups/membership lists (likely the user's real name for identification purposes).
      - admin -> does the user recieve Penn Club Review admin privelages? Useful for bugfixing or QA testing. 
      - created -> the date/time the account was created. Useful for account verificaiton. 
   - Methods:
      - to_dict -> convert a JSON dict to a User object.
      - from_dict (static) -> convert a User object to a JSON dict. Static because the User instance doesn't exist yet. 


## Noteable Design Choices

- Centralized SQLAlchemy instance (single 'db' in 'db_create.py')
   - Why: prevents circular-import problems and accidental creation of multiple 'SQLAlchemy()' instances that triggered many errors for me early on. 

- Models as explicit relationships
   - 'Favorite' is a separate model with keys to 'Club' and 'User' rather than storing a single list on 'Club'.
   - Why: this makes queries more flexible and lets me add metadata (timestamp, source).

- Tag handling
   - Tags are normalized (title-cased) and stored in a separate 'Tag' model with a association table 'club_tags'.
   - Why: this avoids tag duplication and makes it easy to list tags and the number of clubs per tag.

- Some fields are not exposed
   - 'GET /api/users' intentionally avoids returning the user's email and internal id for privacy reasons. Exposing emails or internal ids increases risk of data being harvested or abused.


## Where to improve / next steps

- Add logins, comments, and caching (as mentioned in WRITEUP.md).
