# -*- coding: utf-8 -*-


import logging
import string
from google.appengine.api.labs import taskqueue
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MailHandler(webapp.RequestHandler):
    def post(self):
        client = self.request.get("client")
        formula = self.request.get("formula")
        subject = self.request.get("subject")
        result = self._get_formula_result(formula)
        mail.send_mail(sender="prstcsnpr@gmail.com", to=client, subject=subject, body='', html=result)
        logging.info('Mail to %s for %s' % (client, formula))
            
    def _get_formula_result(self, formula):
        result = urlfetch.fetch(url='http://qmagicformula.appspot.com/'+formula)
        if result.status_code == 200:
            return result.content
        

class PostOfficeHandler(webapp.RequestHandler):
    def post(self):
        client = self.request.get("client")
        formula = self.request.get("formula")
        subject = self.request.get("subject")
        taskqueue.add(url='/tasks/mail',
                      queue_name='mail',
                      params={'client' : client, 'formula': formula, 'subject': subject},
                      method='POST')
    def get(self):
        self.post()
        

application = webapp.WSGIApplication([('/tasks/mail', MailHandler),
                                      ('/tasks/postoffice', PostOfficeHandler)], 
                                     debug=True)


def main():
    run_wsgi_app(application)
    
    
if __name__ == '__main__':
    main()