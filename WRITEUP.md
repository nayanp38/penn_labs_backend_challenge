# Open-Ended Questions

## 1.
To implement signup/login/logout features, I would include three main routes. (1) Sign up. This route would create an account, and maybe include email verification. For email sending, I would use the flask-mail package. (2) Log in. This route would log into an existing account with correct credentials. (3) Sign out. This route would sign out of the account currently logged in. These three routes in particular would use the POST method since we're sending data (credentials) into the database. Those three are essential, however I would a "forgot password" feature to make users' lives easier if I had extra time. 

To make sure the system is safe from hackers, I want to start by making sure passwords is hashed. The package Argon2 (argon2-cffi in Python) would be my pick for doing so. 2FA is another feature I would want to include to keep the system robust. 2FA via email could be implemented using flask-mail above. Other, more secure 2FA methods could be implemented using the webauthn package. 

## 2.
To implement a comment system, I'd want to implement this table: 
- comment
    - represents a single message 
    - attributes:
        - id
        - body -> text in the comment
        - club_id -> club it's under
        - user_id -> author
        - parent_id -> id of a parent comment if it's a reply
        - thread_id -> id of the original comment in the thread
        - created -> time of the comment's creation
    - relationships:
        - club -> connect to the club the comment's under 
        - author -> connect to the user who authored the quote
        - parent -> connect to the parent comment
        - root -> connect to the original comment in the thread

I could also implement a comment_reaction table to include a reaction to a comment, where each user is limited to one reaction per type per comment. For example, a like, laugh, heart, etc. Implementation would be largely similar without the text and thread attributes. 

To instantiate these comments, creating a root comment would be relatively simple, with all the attributes being inputted to a POST request that could create the comment. To create a reply, the process would be similar, however a parent must be added to reflect the reply to the previous comment. By ensuring the root of the thread is associated to every comment, threads could be easily searched for with an API request. 

In total, we'd want the following routes:
- [POST] "/api/clubs/\<code\>/comments" -> create root comment
- [POST] "/api/comments/\<id\>/reply" -> reply to a comment
- [GET] "/api/clubs/\<code\>/comments" -> list comments of a club
- [GET] "/api/comments/\<thread_id\> -> search for a thread
- [POST] "/api/comments/\<id\>/react" -> add reaction
- [DELETE] "/api/comments/\<id\>" -> delete comment

## 3.
Here are the routes I would cache: 
- [GET] "/api/clubs" -> used often and computationally expensive, so caching would save a lot of compute. 
- [GET] "/api/clubs/search" -> computationally expensive. We could cache a search for each letter typed in by the user to make subsequent searches using those prefixes much faster. 
- [GET] "/api/users/\<username\>" -> user profiles don't change often, so we can cache for longer. 
- comment/thread searches -> similar reason to club search, and comments likely won't change too often. 

I'd cache these routes for aroune 1-2 mins. "/api/users/\<username\>" can be cached for much longer since user profiles rarely change. I wouldn't cache the [POST], [PATCH], or [DELETE] requests since those need to be immediately updated when a change is made. 

For caching, I'd use the flask-caching package to easily integrate with our Flask app. 

To make sure we avoid state management concerns, we need to make sure we keep track if the cache is present or not. If it is, we can read from the cache when dealing with changing data. But, if it's not, we should ensure we rebuild directly from the database. To keep track if a cache is present, we can use a verisoning system that labels each cache with a version, and increment the database version whenever a code change is made. If the cache and database version don't match, we know the cache isn't present. We can do this in Python with the Redis package. 

We can also help the problem by using shorter TTLs so the cache refreshes more often. 

