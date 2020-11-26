# python-on-tas
Example Python Rep


Basic python demo with templates and bootstraped GUI. Uses gunicorn to serve the python from CF, so is production ready. 

Use cleardb to bind database to application, the app will detect 

When running locally, create a .env file with the VCAP_SERVICES details. 

Todo:
Seperate Static directory to seperate application so static files are not served by python but by web server. 
