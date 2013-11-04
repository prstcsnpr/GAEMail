# -*- coding: utf-8 -*-


import logging
import string
from google.appengine.api.labs import taskqueue
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MailHandler(webapp.RequestHandler):
    def post(self):
        to = self.request.get("to")
        subject = self.request.get("subject")
        body = self.request.get("body")
        html = self.request.get("html")
        mail.send_mail(sender="prstcsnpr@gmail.com", to=to, subject=subject, body=body, html=html)
        logging.info('Mail to %s' % (to))
        

class PostOfficeHandler(webapp.RequestHandler):
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        postmen = []
        with open('postmen') as file:
            for line in file.readlines():
                postman = line.split()[0]
                postmen.append(postman)
        i = 0;
        with open('clients') as file:
            for line in file.readlines():
                client = line.split()[0]
                postman = postmen[i % len(postmen)];
                taskqueue.add(url=postman,
                              queue_name="mail",
                              method="POST",
                              params={'to' : client,
                                      'subject' : subject,
                                      'body' : '',
                                      'html' : content,
                                      })
                logging.info('Mail to %s by %s' % (client, postman))
                i = i + 1
        


application = webapp.WSGIApplication([('/tasks/mail', MailHandler),
                                      ('/tasks/postoffice', PostOfficeHandler)], 
                                     debug=True)


def main():
    run_wsgi_app(application)
    
    
if __name__ == '__main__':
    main()