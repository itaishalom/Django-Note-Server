# Backend Coding Challenge
Some notes :)

I have implemented everything, a few things that I would want to change in the future:
1. Change from Token to Bearer since Bearer authentication is more advanced and secure.
2. Add 'orderBy' as a query param
3. Tags array, for some reason returned as a comma-separated, by the tags search works with no problem
4. Utilize Elasticsearch, it requires a NoSQL DB
5. I think a better way to save public notes is on a different DB, rather than on the same DB with different values (public/private). Indexing accordingly may result in good query times, but I think it will be safer.


### Application:

* Users can add, delete, and modify their notes
* Users can see a list of all their notes
* Users can filter their notes via tags
* Users must be logged in, in order to view/add/delete/etc. their notes

### The notes are plain text and should contain:

* Title
* Body
* Tags

### Optional Features 🚀

* [X] Search contents of notes with keywords
* [X] Notes can be either public or private
    * Public notes can be viewed without authentication, however they cannot be modified
* [X] User management API to create new users

### Limitations:

* use Python / Django
* test accordingly
