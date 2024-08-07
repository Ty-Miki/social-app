This is an image bookmarking application with many built in features.


### Features

- User Authentication and Authorization,
  - Login, Logut, Passoword change and Password reset options,
  - Custom Authentication backend to authenticate users with both username and email,
  - Social authentication using Facebook and Google.
- User registration with extended user models to accept profile photo and DOB.
  - Checks for existing emails before signing up the user.
- Notify users when they complete certain actions,
  - changing profile,
  - bookmarking an image ...
- Bookmarking an image from any other website,
- AJAX requests to let users like/unlike images and follow/unfollow each other,
- Infinite scroll pagination to images using JavaScript,
- Generic activity stream to let users know what is hapening.
  - Users can see when other users perform certain actions like:
    - A user bookmarks an image,
    - A user likes an image,
    - A user creates an account,
    - A user starts following another user ...
- Django debug toolbar integrated for debugging,
  - is configured to run only when IP address is 127.0.0.1/localhost.
- Counting image views and ranking them by their veiw using Redis.

### Requirements

- All required packages are found in the *requirements.txt* file.


If you want to use this app and need help setting it up I would be happy to help, contact me at mekbibabiro@gmail.com.

**Bye.**
