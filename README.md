Simple grocery list web app using Flask+DynamoDB for the backend. Hosted on AWS.

Front end code is heavily modified from a lesson in [Javascript 30](https://courses.wesbos.com/account/access/5863d196661bae5f4999b00f/view/e3ba3f1664). It is simple HTML+CSS+JS and works on mobile and desktop browsers.

In addition to the code in this repository, you will also need to set up some other services to get the application working:

* Install and set up your virtual environment. I am currently using virtualenv and have included the requirements.txt file.

* Set up routing for the front end of this application and the flask API. If you are using an Apache webserver you can edit your Virtual Hosts file with the command:

    sudo emacs /etc/httpd/conf.d/vhost.conf

    If you are hosting only this application, the file should look like the below where domain is your website domain name, and ‘app.domain.com’ and ‘flask.domain.com’ are the URLs you’d like to use for the front end and Flask API respectively. You’ll need to add the flask API URL to the index.js file URLRemote variable.

```    
    NameVirtualHost *:80

    <VirtualHost *:80>
        DocumentRoot /var/www/GroceryList
        ServerName app.domain.com

    </VirtualHost>

    <VirtualHost *:80>
            DocumentRoot /var/www/GroceryList
            ServerName flask.domain.com

            WSGIDaemonProcess GroceryList user=username group=groupname threads=5
            WSGIScriptAlias / /var/www/GroceryList/deploy.wsgi

            <directory /var/www/GroceryList>
                    WSGIProcessGroup GroceryList
                    WSGIApplicationGroup %{GLOBAL}
                    WSGIScriptReloading On
                    Order deny,allow
                    Allow from all
            </directory>
    </VirtualHost>
```

* Set up the subdomains there to ensure they point to your server correctly. 

* Create a table in DynamoDB using:

    Primary partition key	GUID (String)
    Primary sort key	ShopDate (String)
    I also suggest unchecking default settings and auto scaling. Use 1 for read and write capacity units to save costs unless you are planning to drastically expand usage of this app.

* Assign the TABLE_NAME variable in groc.py to whatever you name your table in DynamoDB.


