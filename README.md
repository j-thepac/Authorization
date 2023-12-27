# API Authorization

## Basic Authentication 
1. Cannot Logout
2. Credential stored in Cache
3. Will expire once browser is closed 
4. from flask_httpauth import HttpBasicAuth
5. Easy to hack 


## Token
1. Stored as Cookies
2   App send usn/pass
    API check credentials in DB
        If a user is found, it generates a token 
        Send token 
    App uses token from now
3. Types : Bearer (life  >15 mins ) , JWT (life < 15 mins )
    Bearer -
        1. life  >15 mins
        2. stored in DB and verified each time
        3. Hard to hack
    JWT  - 
        1. Life is 15 mins
        2. Carries all info
        3. Once issued hard to invalide
        4. Hard to Hack 

### Browser > Console 

    document.cookie
    document.cookie = 'csrftoken='