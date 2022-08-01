# Like friends photos vk

The application allows you to like photos of friends on Vkontakte
***

## How to use

To like photos, you need to log in. This can be done using the `login and password` from the VK account and the `access token` that you need to get.
(*The login and password are not saved by the application. Only a temporary access token is saved*).

## Auth by login and password
In the menu, select `Auth`->`Auth by password`. Then enter the data and press the button. 
In case of `successful authorization`, information about the user will be displayed on the main form.

<img width="252" alt="image" src="https://user-images.githubusercontent.com/78900834/182235115-d1270d44-4730-4f94-b87a-d1032a01b663.png"> <img width="241" alt="image" src="https://user-images.githubusercontent.com/78900834/182235175-090193e6-e487-485a-9c01-ef8d4db3620f.png">

Otherwise, a message about `incorrect data` and advice to try using the `access token`.

## Auth by access token
In the menu, select `Auth`->`Auth by access token`.

Then there will be a short instruction:
1. Go to the website
2. Allow access
3. Enter the url of the page to be redirected to

<img width="342" alt="image" src="https://user-images.githubusercontent.com/78900834/182236046-81966838-35c7-4b3a-bd17-57fb4d9c1fbf.png">

The site to go to and give permission to.
<img width="789" alt="image" src="https://user-images.githubusercontent.com/78900834/182236113-8b4025ab-60c9-4f6d-ab4b-c7af266d2bb5.png">
<img width="806" alt="image" src="https://user-images.githubusercontent.com/78900834/182236277-54331881-82be-4c94-bf80-e173e04fdf72.png">

After that, you need to `copy` the entire `url` of the page and `paste` it into the `field` on the form.
<img width="342" alt="image" src="https://user-images.githubusercontent.com/78900834/182236918-093bbe10-f30c-48e7-92d9-053208cd2ae0.png">

## Language
The application is available in Russian and English.
In the `menu`, you can select the desired language.

<img width="124" alt="image" src="https://user-images.githubusercontent.com/78900834/182238272-2cb34bd0-9cb5-4b05-bdc9-ff8cda9e0fb5.png">

## Albums
First you need to choose the `owner` of the `album` (friend or yourself) and click 'Show albums`. 
After that, the `albums available` to you and the `number of photos` in it will be displayed in the `album list`.
<img width="569" alt="image" src="https://user-images.githubusercontent.com/78900834/182239351-b5f0b0d0-e911-4302-b5cc-ecb6aa001c69.png">

## Liking photos
You need to `select an album` and click the button `Put likes` to like all photos or `Remove likes` to remove likes from them.
In the lower part of the form, the `name of the operation`, its `progress` and the `cancel button` are displayed. After the operation is `completed successfully`, 
a message will be displayed.

<img width="356" alt="image" src="https://user-images.githubusercontent.com/78900834/182240582-8c13dc0c-60f6-4257-a712-2ab2272899b2.png"> <img width="305" alt="image" src="https://user-images.githubusercontent.com/78900834/182240845-0975c6c7-4f81-4235-8924-4022dfc4cd11.png">

After a `large number` of requests, you will need to enter the `captcha text` to continue the operation.

<img width="250" alt="image" src="https://user-images.githubusercontent.com/78900834/182241282-1f84d9f3-86f6-45cc-b8cd-1b6b32e29a29.png">

## Application Technologies
The forms are created using `Tkinter`. But for the user interface, you can make another option.

`Gettext` is used for localization. It is very easy to add a new language:
1. Based on a template (**file: like.pot**), using (for example, the `Poedit` program), create a new language variant.
2. Save to the directory `handlers\languages\locale\` with the abbreviation of the language (for example, `es`) and the folder `\LC_MESSAGES`.
3. Create a new `FooLanguage` class that inherits the abstract `Language` class.
4. Create an instance in the `MainHandler`.
