# comfucius-instagram

The software I use for posting ~~spam~~ beautiful motivational poster on our ~~preferred social network~~ Instagram.

Motivational poster are made using fake quote phrase from [Comfucius website](https://comfucius.xyz) in that moment, and a list of "weird" hashtag taken from a local SQLite database.

![Example](.assets/sei-mejo-poster.jpg)

## Deploy instruction

1. Install python, version 3
2. Install python dependencies
   1. (Optional but suggested) - Use venv (virtualenv) to create a virtual python env
   2. `cd` into project root folder and do `pip install -r requirements.txt`
3. Create the local hashtag database
   1. Install `sqlite3`
   2. `cd` into project root folder and use sqlite3 to create DB
      1. `sqlite3 database.sqlite`
      2. `.import --csv --skip 4 flat_file_database.csv hashtag`

4. Launch `do_damage.py` to create a motivational poster and save it locally, if "DRY_RUN" is "true"
   - BEWARE: In DRY_RUN mode, image is NOT deleted from disk!  
5. (Optional - Actual create a post on Instagram)
   1. Deactivate "DRY_RUN", setting it to "false"
   2. Set your actual Instagram username/password
      1. (Proper, better option) Set them into your machine environment variables
         1. Delete '.env' file from project root folder, or simply blank username/password related values within
         2. Set "INSTAGRAM_USERNAME" and "INSTAGRAM_PASSWORD" environment variable with...former and latter values
            - [Don't forget that storing secrets into environment variable is a bad practice](https://stackoverflow.com/questions/12461484/is-it-secure-to-store-passwords-as-environment-variables-rather-than-as-plain-t)
      2. (quick and dirty) Set local dotenv file
         1. Open '.env' file from project root folder
         2. Set "INSTAGRAM_USERNAME" and "INSTAGRAM_PASSWORD" environment variable with...former and latter values
   3. (Optional but very useful) Dump a valid Instagram cookie to avoid IP banning or OTP prompt
      1. TODO
   4. Launch `do_damage.py`. Poster image will be saved locally and then posted online. After that, it will be deleted from local disk.

## LICENSE

Check 'LICENSE' file for references and licence about current scripts and code.

Images used for poster making are taken from [Unsplash](https://unsplash.com). They are too many to be cited individually, [check the Unsplash collection to see them all](https://unsplash.com/it/collezioni/10453773/backgrounds-that-inspired-comfucius).

Fonts are licensed under "SIL Open Font License". License file is within the "font" folder.
