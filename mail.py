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
        if 'magicformula' == formula:
            magic = self._get_magic_formula_result()
            mail.send_mail(sender="prstcsnpr@gmail.com", to=client, subject='神奇公式', body='', html=magic)
            logging.info('Mail to %s for MagicFormula' % (client))
        if 'grahamformula' == formula:
            graham = self._get_graham_formula_result()
            mail.send_mail(sender="prstcsnpr@gmail.com", to=client, subject='格雷厄姆公式', body='', html=graham)
            logging.info('Mail to %s for GrahamFormula' % (client))
        
    def _get_magic_formula_result(self):
        result = urlfetch.fetch(url='http://qmagicformula.appspot.com/magicformula')
        if result.status_code == 200:
            return result.content
        
    def _get_graham_formula_result(self):
        result = urlfetch.fetch(url='http://qmagicformula.appspot.com/grahamformula')
        if result.status_code == 200:
            return result.content

class PostOfficeHandler(webapp.RequestHandler):
    def post(self):
        client = self.request.get("client")
        formula = self.request.get("formula")
        taskqueue.add(url='/tasks/mail',
                      queue_name='mail',
                      params={'client' : client, 'formula': formula},
                      method='POST')
        

application = webapp.WSGIApplication([('/tasks/mail', MailHandler),
                                      ('/tasks/postoffice', PostOfficeHandler)], 
                                     debug=True)


def main():
    run_wsgi_app(application)
    
    
if __name__ == '__main__':
    main()