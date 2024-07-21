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

##### Sitemap

- admin/ - use this url to navigate the admin interface,
- account/ - use this url to navigate user Authenticatin and/or Authorization pages,
  - Logging in, Logging out, Changing password and Reseting Password,
  - account/ - user dashboard,
  - account/register - to create a new account,
  - account/edit - to edit user profile.
- social-auth - for SSO services.
