#!/usr/bin/env python
"""jet.py: Jason's Email Tester , Simple IMAP,POP,SMTP CLI Tester"""

__author__ = "Jason Stokes"
__copyright__ = "Copyright 2018"
__credits__ = ["Jason Stokes"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jason Stokes"
__email__ = "j32493@gmail.com"
__status__ = "Production"

import imaplib
import smtplib
import poplib
import time
import datetime
import re

class settings():
    def __init__(self):
        self.tko = 30
        self.server = ""
        self.smtp_server = ""
        self.email_address = ""
        self.user = ""
        self.psw = ""
        self.imap_ssl_port = 993
        self.imap_port = 143
        self.pop_ssl_port = 995
        self.pop_port = 110
        self.smtp_port = 25
        self.smtp_ssl_port = 465
        self.smtp_to = self.user
        self.smtp_subject = "This is a test for smtp"
        self.smtp_body = "This is a test for smtp. Sent from Jason's email Test"
        self.smtp_ssl_subject = "This is a test for smtp with ssl"
        self.smtp_ssl_body = "This is a test for smtp with ssl. Sent from Jason's email Test"
        self.test_imap = False
        self.test_pop = False
        self.test_smtp = False
        self.test_imap_ssl = False
        self.test_pop_ssl = False
        self.test_smtp_ssl = False
        self.imap_results = False
        self.imap_ssl_results = False
        self.pop_results = False
        self.pop_ssl_results = False
        self.smtp_results = False
        self.smtp_ssl_results = False
        self.aod = []
        self.aot = []
        self.debug_output = False
        self.smtp_auth = True

    def setup(self):
        self.server = require_input("Server")
        self.email_address = email_input("Email Address: ")
        self.user = raw_input("User ({0}):".format(self.email_address)) or self.email_address
        self.psw = require_input("Password: ")
        self.smtp_to = self.email_address
        self.smtp_server = self.server

        test_all = yes_or_no("Test all with defaults ")
        if test_all == True:
            self.test_imap = True
            self.test_pop = True
            self.test_smtp = True
            self.test_imap_ssl = True
            self.test_pop_ssl = True
            self.test_smtp_ssl = True
            self.show_settings()
            return True

        self.test_imap = yes_or_no("Test IMAP ")
        if self.test_imap == True:
            self.imap_port = raw_input("Port (143) : ") or 143

        self.test_imap_ssl = yes_or_no("Test IMAP SSL ")
        if self.test_imap_ssl == True:
            self.imap_ssl_port = raw_input("Port (993) : ") or 993

        self.test_pop = yes_or_no("Test POP3 ")
        if self.test_pop == True:
            self.pop_port = raw_input("Port (110) : ") or 143

        self.test_pop_ssl = yes_or_no("Test POP3 SSL ")
        if self.test_pop_ssl == True:
            self.pop_ssl_port = raw_input("Port (995) : ") or 995

        self.test_smtp = yes_or_no("Test SMTP ")
        if self.test_smtp == True:
            self.smtp_port = raw_input("Port (25) : ") or 25

        self.test_smtp_ssl = yes_or_no("Test SMTP SSL ")
        if self.test_smtp_ssl == True:
            self.smtp_ssl_port = raw_input("Port (465) : ") or 465

        if self.test_smtp or self.test_smtp_ssl:
            self.smtp_server = raw_input("Server ({0}): ".format(self.smtp_server)) or self.smtp_server
            self.smtp_auth = yes_or_no("Do authentication ")
            self.smtp_to = raw_input("Send Test, TO ({0}): ".format(self.user)) or self.user

        self.debug_output=yes_or_no("Debug output?",True)
        self.show_settings()

    def show_settings(self):
        print("\nCurrent Settings")
        print("--------------------------------------------------")

        self.printer("Server",self.server)
        self.printer("User",self.user)
        self.printer("Password",self.psw)

        self.printer("IMAP",self.test_imap)
        self.printer("IMAP Port",self.imap_port)

        self.printer("IMAP SSL",self.test_imap_ssl)
        self.printer("IMAP SSL Port",self.imap_ssl_port)

        self.printer("POP3",self.test_pop)
        self.printer("POP3 Port",self.imap_port)

        self.printer("POP3 SSL",self.test_pop_ssl)
        self.printer("POP3 SSL Port",self.pop_ssl_port)

        self.printer("SMTP",self.test_smtp)
        self.printer("SMTP Port",self.smtp_port)

        self.printer("SMTP SSL",self.test_smtp_ssl)
        self.printer("SMTP SSL Port",self.smtp_ssl_port)
        self.printer("SMTP Server",self.smtp_server)
        self.printer("Send Test Mail To",self.smtp_to)
        self.printer("SMTP AUTH",self.smtp_auth)

        self.printer("DEBUG Output",self.debug_output)

        print("")


        ok_settings=yes_or_no("Are These Settings Correct")

        if not ok_settings:
            self.setup()
        pass

    def printer(self,k,v):
        if v == True:
            v = "OK"
        if v == False:
            v = "NO"
        print('{0:>20s} : {1}'.format(k,v))
        return True

    def show_results(self):
        print("\n\nRESULTS")
        print("--------------------------------------------------")
        for x in self.aot:
            print("{0} : {1:8s} : {2}\n ".format(x['dt'].strftime("%A, %d. %B %Y %I:%M%p"), x['section'] ,x['event']))

        if self.aod:
            print("\n\nERRORS")
            print("--------------------------------------------------")
            for x in self.aod:
                print("{0} : {1:8s} : {2:10} {3}\n".format(x['dt'].strftime("%A, %d. %B %Y %I:%M%p"), x['section'] ,x['location'],x['error']))
        return True

    def handle_errors(self,section,location,errorc):
        dt = datetime.datetime.now()
        self.aod.append({"section":section,"location":location,"error":errorc,"dt":dt})
        return True

    def handle_logs(self,section,location,event):
        dt = datetime.datetime.now()
        self.aot.append({"section":section,"location":location,"event":event,"dt":dt})
        return True

def yes_or_no(question,n = False):
    if not n:
        reply = str(raw_input(question+' (Y / n): ') or "y").lower().strip()
    else:
        reply = str(raw_input(question+' (y / N): ') or "n").lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Try Again: {0}".format(question))

def require_input(question):
    r = str(raw_input("{0} :".format(question)))
    if r and r.strip():
        return r
    else:
        print("Please Answer the question")
        return require_input(question)

def email_input(question):
    ri = str(raw_input("{0} :".format(question)))
    ri = ri.strip()
    if re.match(r"[^@]+@[^@]+\.[^@]+",ri):
        return ri
    else:
        print("Enter Valid Email")
        return require_input(question)

def debug_print(s,output):
    if s.debug_output:
        print(output)
    return True

def imap_test(s):
    print("Running Imap test")
    try:
        debug_print(s,"connecting to {0}:{1}".format(s.server,s.imap_port))
        m = imaplib.IMAP4(s.server,s.imap_port)
    except imaplib.IMAP4.error as er:
        debug_print(s,"IMAP Connection failed")
        msg = er.args[0]
        s.handle_errors('IMAP','connection',)
        s.handle_logs('IMAP','test','failed : {0}'.format(msg))
    else:
        try:
            debug_print(s,"Logging In as {0} with Password: {1}".format(s.user,s.psw))
            m.login(s.user,s.psw)
        except imaplib.IMAP4.error as er:
            msg = er.args[0]
            debug_print(s,"Log in failed")
            s.handle_errors('IMAP','login',msg)
            s.handle_logs('IMAP','test','failed : {0}'.format(msg))
        else:
            debug_print(s,"Log in successful")
            s.handle_logs('IMAP','connection','logged in')
            s.imap_results = True
            s.handle_logs('IMAP','test','passed')
        m.logout();
        debug_print(s,"Logged out of IMAP")
    return True

def imap_ssl_test(s):
    print("Running Imap SSL test")
    try:
        debug_print(s,"connecting to {0}:{1}".format(s.server,s.imap_ssl_port))
        m = imaplib.IMAP4_SSL(s.server,s.imap_ssl_port)
    except imaplib.IMAP4.error as er:
        debug_print(s,"IMAP SSL Connection failed")
        debug_print(s,imaplib.IMAP4.error)
        msg = er.args[0]
        s.handle_logs('IMAP SSL','test','failed : {0}'.format(msg))
    else:
        try:
            debug_print(s,"Logging In as {0} with Password: {1}".format(s.user,s.psw))
            m.login(s.user,s.psw)
        except (imaplib.IMAP4.error) as er:
            debug_print(s,"Log in failed")
            msg = er.args[0]
            s.handle_errors('IMAP SSL','login',msg)
            s.handle_logs('IMAP SSL','test','failed : {0}'.format(msg))
        else:
            debug_print(s,"Log in successful")
            s.imap_ssl_results = True
            s.handle_logs('IMAP SSL','test','passed')
        m.logout();
        debug_print(s,"Logged out of IMAP SSL")
    return True

def pop_test(s):
    msg = ""
    print("Running POP test")
    try:
        debug_print(s,"connecting to {0}:{1}".format(s.server,s.pop_port))
        m = poplib.POP3(s.server,s.pop_port)
    except (poplib.error_proto),msg:
        debug_print(s,"Connection failed")
        debug_print(s,msg)
        s.handle_errors('POP3','connection',msg)
        s.handle_logs('POP3','test','failed : {0}'.format(msg))
    else:
        try:
            debug_print(s,"Logging In as {0} with Password: {1}".format(s.user,s.psw))
            m.user(s.user)
            m.pass_(s.psw)
        except (poplib.error_proto) ,msg:
            debug_print(s,"Log in failed")
            debug_print(s,msg)
            s.handle_errors('POP3','login',msg)
            s.handle_logs('POP3','test','failed : {0}'.format(msg))
        else:
            debug_print(s,"Log in successful")
            mc,ms = m.stat()
            debug_print(s,"count = {0} , size = {1}".format(mc,ms))
            s.pop_results = True
            s.handle_logs('POP3','test','passed')
        m.quit();
        debug_print(s,"Logged out of POP")

def pop_ssl_test(s):
    msg = ""
    print("Running POP test")
    try:
        debug_print(s,"connecting to {0}:{1}".format(s.server,s.pop_ssl_port))
        m = poplib.POP3_SSL(s.server,s.pop_ssl_port)
    except (poplib.error_proto),msg:
        debug_print(s,"Connection failed")
        debug_print(s,msg)
        s.handle_errors('POP3 SSL','connection',msg)
        s.handle_logs('POP3 SSL','test','failed : {0}'.format(msg))
    else:
        try:
            debug_print(s,"Logging In as {0} with Password: {1}".format(s.user,s.psw))
            m.user(s.user)
            m.pass_(s.psw)
        except (poplib.error_proto) ,msg:
            debug_print(s,"Log in failed")
            debug_print(s,msg)
            s.handle_errors('POP3 SSL','login',msg)
            s.handle_logs('POP3 SSL','login','failed : {0}'.format(msg))
        else:
            debug_print(s,"Log in successful")
            mc,ms = m.stat()
            debug_print(s,"count = {0} , size = {1}".format(mc,ms))
            s.handle_logs('POP3 SSL','test','passed')
        m.quit();
        debug_print(s,"Logged out of POP SSL")
        s.pop_results = True
    return True

def smtp_test(s):
    msg = ""
    print("Running SMTP (No AUTH).")
    debug_print(s,"connecting to {0}:{1}".format(s.smtp_server,s.smtp_port))
    timesent = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    outgoing = """Subject: {2}


    To: {0}
    From: {1}
    Server: {4}
    Port: {5}
    Time Sent: {6}
    {3}
    """.format(s.smtp_to,s.user,s.smtp_subject,s.smtp_body,s.smtp_server,s.smtp_port,timesent)
    try:
        sm = smtplib.SMTP(s.smtp_server,s.smtp_port,None,s.tko)
        sm.ehlo()
        sm.sendmail(s.user,s.smtp_to,outgoing)
        sm.quit()
    except smtplib.SMTPException as er:
        msg = str(er)
        s.handle_errors('SMTP no Auth','connection',msg)
        s.handle_logs('SMTP no Auth','test','failed : {0}'.format(msg))
        sm.quit()
    except smtplib.socket.error:
        s.handle_errors('SMTP no Auth','connection','Timeout')
        s.handle_logs('SMTP no Auth','test','failed')
    else:
        s.handle_logs('SMTP no Auth.','test','passed')

    msg = ""
    print("Running SMTP (AUTH)")

    try:
        sm = smtplib.SMTP(s.smtp_server,s.smtp_port,None,s.tko)
        sm.set_debuglevel(True)
        sm.ehlo()
        if sm.has_extn('STARTTLS'):
            tls = True
            sm.starttls()
            sm.ehlo()
            debug_print(s,"Using TLS")
            s.handle_logs('SMTP','connection',"Using TLS")
        if s.smtp_auth:
            s.handle_logs('SMTP','login',"Trying With Auth")
            sm.login(s.user, s.psw)
        sm.sendmail(s.user,s.smtp_to,outgoing)
        sm.quit()
    except smtplib.SMTPException as er:
        msg = str(er)
        s.handle_errors('SMTP','connection',msg)
        s.handle_logs('SMTP','test','failed : {0}'.format(msg))
    except smtplib.socket.error:
        s.handle_errors('SMTP','connection','Timeout')
        s.handle_logs('SMTP','test','failed')
    else:
        cc = "SMTP"
        if tls:
            cc = "SMTP w/ TLS"
        s.handle_logs(cc,'test','passed')
    return True

def smtp_ssl_test(s):
    msg = ""
    print("Running SMTP SSL test")
    debug_print(s,"connecting to {0}:{1}".format(s.smtp_server,s.smtp_ssl_port))
    timesent = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

    outgoing = """Subject: {2}


    To: {0}
    From: {1}
    Server: {4}
    Port: {5}
    Time Sent: {6}
    {3}
    """.format(s.smtp_to,s.user,s.smtp_subject,s.smtp_ssl_body,s.smtp_server,s.smtp_ssl_port,timesent)
    try:
        sm = smtplib.SMTP_SSL(s.smtp_server,s.smtp_ssl_port,None,None,None,s.tko)
        sm.ehlo()
        if sm.has_extn('STARTTLS'):
            tls = True
            sm.starttls()
            sm.ehlo()
            print("Using TLS")
            s.handle_logs('SMTP','connection',"Using TLS")
        if s.smtp_auth:
            s.handle_logs('SMTP','login',"Trying With Auth")
            sm.login(s.user, s.psw)
        sm.sendmail(s.user,s.smtp_to,outgoing)
        sm.quit()
    except smtplib.SMTPException as er:
        msg = str(er)
        s.handle_errors('SMTP SSL','connection',msg)
        s.handle_logs('SMTP SSL','test','failed : {0}'.format(msg))
        sm.quit()
    except smtplib.socket.error:
        s.handle_errors('SMTP SSL','connection','Timeout')
        s.handle_logs('SMTP SSL','test','failed , timeout')
    else:
        s.handle_logs('SMTP SSL','test','passed')
    return True

def run_tests(s):
    print("")
    start_now = yes_or_no("Start Now? ") or "y"
    if not start_now:
        return False

    if s.test_imap:
        imap_test(s)
        time.sleep(1)

    if s.test_imap_ssl:
        imap_ssl_test(s)
        time.sleep(1)

    if s.test_pop:
        pop_test(s)
        time.sleep(1)

    if s.test_pop_ssl:
        pop_ssl_test(s)
        time.sleep(1)

    if s.test_smtp:
        smtp_test(s)
        time.sleep(1)

    if s.test_smtp_ssl:
        smtp_ssl_test(s)
        time.sleep(1)

    return True


print("\nJason's Email Tester\n")
ts = settings()
ts.setup()
run_tests(ts)
ts.show_results()
