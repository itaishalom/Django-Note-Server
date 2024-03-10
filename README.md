# Backend Coding Challenge
Some notes :)

I have implemented everything, a few things that I would want to change in the future:
1. Change from Token to Bearer since Bearer authentication is more advanced and secure.
2. Add 'orderBy' as a query param
3. Tags array, for some reason returned as a comma-separated, by the tags search works with no problem
4. Utilize Elasticsearch or MongoDB, better for text search (as it's one of the requirements)  including advanced indexing and ranking algorithms
5. I think a better way to save public notes is on a different DB, rather than on the same DB with different values (public/private). Indexing accordingly may result in good query times, but I think it will be safer.
6. Alongside the tests in the file tests, I wrote another e2e test to mimic a real client-backend flow because in my experience, sometimes the backend developer doesn't always understand how to frontend uses their API so in my opinion it is very important, check client_test.py.
7. Extracted some business logic to the utils class, but if there is a need for more business logic, I would create a controller-like class to handle it, although Django follows an MTV pattern where the views act as controllers.
8. I didn't create templates i.e. HTML files, just a backend.
9. If I had more time, I would implement a Flutter app with this project.

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
