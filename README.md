# Social Application

### Objective

To build a social application that will allow users to share images that they find on the internet.

### Requirements

- Authentication system: to register, login and change or reset passwords.
- A follow system: to allow users follow each other on the website.
- A system for users to share images from any website.
- An activity stream that allows users to see the content uploaded by users that they follow.

#### 1. Authentication system

    For logging in, logging out, changing password and resetting password I used django's authentication system which is found in the*django.contrib.auth* application.

    I have used django's built in authentication views which can be found at https://docs.djangoproject.com/en/5.0/topics/auth/default/#all-authentication-views.

    I have added a registration method for users to create a new account. When a user creates a new account a Profile model will be assciated to them where they can add 	date of birth and photo. for this purpose I used a registration form, a view and two templates (register.html and register_done.html) for registration and a custom model name Profile for user profile. plus users are able to edit their profile once they are logged in.

    I have used django's**messages** framework to display success and error messages during profile editing.

    Users can authenticate using their username or email. for email authentication I have used a custome authentication backend and added it to AUTHENTICATION_BACKENDS attribute of settings.py. I have also applied methods to restrict users from using exsiting email addresses during registering and editing their profiles.

I have added a social authentication system to allow users use SSO services from Facebook and Google.

#### 2. Sharing content

- This is a system to let users share images ( either by uploading or by bookmarking from other websites ) and to let them like the images posted by other users.
- The requriements for this are:
  - A data model for images must be created with one-to-many relationship with a user, many-to-many relatioship with user likes and other fields like title, slug, URL, image (to save the actual image in the database) and description.
  - A form and a view to let users share/bookmark images from other websites.
    - For this purpose a Javascript bookmarklet is required, which can run on any website and let users bookmark images from them.

Note: The javascript bookmarklet works as follows.

- The user drags a link from the django server to their bookmarks bar.
  - This link contains Javascript code in its href attribute, so the code will be stored in the bookmark.
  - Then the user naviagtes to any website and clicks on the bookmark which will excute the Javascript code.

Additionally Javascript AJAX requests are used for **liking or unliking** images and **infinite pagination list** for images.

#### 4. User actions

- A follow system is added using a Django view and JavaScript AJAX request using the fetch() API.

##### Sitemap

- admin/ - use this url to navigate the admin interface,
- account/ - use this url to navigate user Authenticatin and/or Authorization pages,
  - Logging in, Logging out, Changing password and Reseting Password,
  - account/ - user dashboard,
  - account/register - to create a new account,
  - account/edit - to edit user profile.
- social-auth - for **SSO** services.
