# imageapi
The image hosting Flask App

## Notes
Images on the server must be one size. Otherwise qualtrics rescales the images and the click locations are screwed up.

## Configuring the server from scratch

### Set up server

- Install Flask `pip install Flask`
- Follow deployment instructions in [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment) I used the mod_wsgi option, so I've included the wsgi file in the imageapi directory.
- Web server data is at `/usr/local/www/apache24/data`
- Config file is at `/usr/local/etc/httpd.conf`

    WSGIDaemonProcess imagesapi
    WSGIScriptAlias /sunspot/imageapi /usr/local/www/apache24/data/imageapi/imageapi.wsgi

    <Directory /usr/local/www/apache24/data/imageapi>
        WSGIProcessGroup images-i
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

### Set up database

- On FreeBSD system, `pkg install sqlite3`
- Run `imageapi/imageapi/load_new_data.sh <csv_file>`
- Make sure all database and all directories above database (imageapi and imageapi/imageapi) have write permissions

### Test configuration

- `http://arpg.colorado.edu/imageapi/landmarks?n=3`

### Debugging 
 
- Server logs are at `/var/log/httpd-error.log` 

