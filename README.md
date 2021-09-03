# Instagram API Clone

![](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter) 

![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


#### Introduction
This API tries to replicate the functions of Instagram.

#### Authentication
The API uses the [Django TokenAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication "Django TokenAuthentication") system.

#### Status Codes
(They can be more than those listed, subject to change)

| Status Code | Description |
| ------------ | ------------ |
| 200 | `OK` |
| 201 | `CREATED` |
| 204 | `NOT CONTENT` |
| 400 | `BAD REQUEST` |
| 403 | `FORBIDDEN` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |



The response can contain data with a `'detail'` key with a list containing the description of the problem (in index 0).

Example:
`{'detail': ["The photo doesn't exist."] }`

## Users

#### Create users
```http
POST /users/signup/
```
The needed values for creating user accounts are the ones from the user, the profile information its not required when creating a user.

| Form Keys |
| ------------ |
| username |
| email |
| password |
| password_confirmation |
| first_name |
| last_name |

#### Validate user
```http
POST /users/verify/
```
After the POST request to `/users/signup/` a email will be send to the user, it will contain a JWT Token for email verification (The token will expire 3 days after being created)

| Form Keys |
| ------------ |
| token |

#### Login user
```http
POST /users/verify/
```
The response will contain the user information and the token for authentication, as following:

```
{
    "user": {
        "username": "foo",
        "email": "foo@bar.com",
        "first_name": "foo",
        "last_name": "bar",
        "profile": {
            "picture": "",
            "biography": ""
        }
    },
    "token": "80x124f275ff8e31193b48ac443b9b72b8ea26t4"
}
```

| Form Keys |
| ------------ |
| username |
| password |


#### Retrieve user
```http
GET /users/`username`/
```
This will retrieve the user information, as following:

```
{
    "user": {
        "username": "foo",
        "email": "foo@bar.com",
        "first_name": "foo",
        "last_name": "bar",
        "profile": {
            "picture": "",
            "biography": ""
        }
    }
}
```

Only the account owner will have authorization to retrieve the user information.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### List users
```http
GET /users
```
This will get a list of all the users, filters can be applied as query strings.

```
[
    {
        "username": "Nicolas",
        "email": "nicolas@domain.com",
        "first_name": "Nicolas",
        "last_name": "Repetto",
        "profile": null
    }
	...
]
```

For filtering the following parameters can be aplied in the url:

| Filter by | Options |
| ------------ | ------------ |
| Search | `username`/`email`/`first_name`/`last_name` |
| Ordering | `first_name`/`last_name` |

#### Update users/profiles
```http
PUT /users/`username`/u/
PATCH /users/`username`/u/
PUT /users/`username`/p/
PATCH /users/`username`/p/
```

The update of the user and profile is done in different requests, the difference is in the last  `/u/` (For user) and `/p/` (For profile). Both PUT and PATCH are accepted.

| Form Keys for User |
| ------------ |
| username |
| email |
| first_name |
| last_name |

| Form Keys for Profile |
| ------------ |
| picture |
| biography |

#### Delete user
```http
DELETE /users/'username'/
```

This will deactivate the user, it will not be deleted from the database.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

## Photos
#### Create photo
```http
POST /photos/
```
This request will create a photo, and return it.
Anyone who is logged in can create a photo.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

The only required field is the image.

| Form Keys |
| ------------ |
| image |
| description |

#### Retrieve photo
```http
GET /photos/'id'/
```
This will retrieve the photo information, as following:
```
{
    "photo": {
        "user": "foo",
        "image": ".../media/photos/photo.jpg",
        "description": "Spam ham",
        "total_likes": 1,
        "total_comments": 0
    }
}
```
Anyone who is logged in can retrieve a photo.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### Update photo description
```http
PATCH /photos/'id'/
```
Only the description of a photo can be changed.

Only the user who created the photo can update it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

| Form Keys |
| ------------ |
| description |

#### Delete photo
```http
DELETE /photos/'id'/
```

Only the user who created the photo can delete it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

## Comments
#### Create comment
```http
POST /photos/'id'/comments/
```
Anyone who is logged in can create a comment. 

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

| Form Keys |
| ------------ |
| comment |

#### Retrieve comment
```http
GET /photos/'id'/comments/'id'/
```
This will retrieve a single comment, as following:
```
{
    "user": "foo",
    "photo": 71,
    "comment": "Look that"
}
```
Anyone who is logged in can retrieve a photo.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### List comments
```http
GET /photos/'id'/comments
```
This will get a list of all the comments in a particular photo, as following:

```
[
    {
        "user": "nicolas",
        "photo": 30,
        "comment": "Something"
    },
	...
]
```
Anyone who is logged in can list the comments of a photo.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### Delete photo
```http
DELETE /photos/'id'/comments/'id'/
```

Only the user who created the comment can delete it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

## Likes
#### Create like
```http
POST /photos/'id'/likes/
```
Anyone who is logged in can create a like. 

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### List likes
```http
GET /photos/'id'/likes
```
This will get a list of all the likes in a particular photo, as following:

```
[
    {
        "user": "foo",
        "photo": 71
    },
	{
        "user": "bar",
        "photo": 71
    },
	...
]
```
Anyone who is logged in can list the comments of a photo.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

#### Delete like
```http
DELETE /photos/'id'/likes/'id'/
```

Only the user who created the like can delete it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |
