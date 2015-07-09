import httplib, urllib2, cookielib, urllib, traceback
import random, StringIO, gzip, six, tempfile, mimetypes
from os import SEEK_END

"""             


              HTTP CLASS WRITTEN IN PYTHON
                      VERSION 2.6                      
   
              Written by Raymond Hernandez
                
              
              (http://www.raysoftinc.com)
              
              
              
              
   
"""

 
"""

		HTTP Object for handling HTTP/s Requests

"""
class HTTP:
	def __init__(self):
		""" Class variables to be set by user """
		# Default user agent  (Internet Explorer 9.0)
		self.UserAgent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
		self.AcceptEncoding = "identity"
		self.KeepAlive = False
		if self.KeepAlive:
			self.connection = "keep-alive"
		else:
			self.connection = "close"
		# Build Default Headers (can be edited)
		self.Headers = { "User-Agent" : self.UserAgent,
		"Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0." + str(random.randint(1,9)) + ",text/plain;q=0." + str(random.randint(1,9)) + ",text/png,*/*;q=0." + str(random.randint(1,9)),
		"Accept-Language" : "en-us,en;q=0." + str(random.randint(1,9)),
		"Accept-Encoding" : self.AcceptEncoding,
		"Connection" : self.connection }
		self.UseProxies = False
		self.HandleRedirects = True
		self.DebugMode = False
		self.CookieDump = ""
		self.ProxyData = ""
		self.Timeout = 60
		self.Tries = 1
		""" Variables not to be used by user """
		self.BuiltOpener = False
		self.Jar = cookielib.CookieJar()
		self.Cookies = urllib2.HTTPCookieProcessor(self.Jar)
		self.Opener = urllib2.build_opener(self.Cookies)
		self.Location = ""
		self.DebugHandler = None
		self.ExtraCookies = []
		self.ExtraHeaders = []
	"""
	
				HTTP REQUEST METHODS   /  PUBLIC METHODS
	
	"""
	def GetRequest(self, url, xmlrequest=False):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				request = urllib2.Request(url, headers=self.Headers)
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "GET: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def PostRequest(self, url, postdata, json=False, xmlrequest=False):
		html =""
		for x in xrange(0, self.Tries):
			self.ResetHeaders()
			try:
				if json == False:
					self.Headers['Content-Type'] = "application/x-www-form-urlencoded"
				else:
					self.Headers['Content-Type'] = 'application/json'
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				self.Headers['Content-Length'] = str(len(postdata))
				request = urllib2.Request(url, postdata, headers=self.Headers)
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "POST: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def PutGetRequest(self, url, xmlrequest=False):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				#self.Headers['Content-Type'] = "application/x-www-form-urlencoded"
				request = urllib2.Request(url, headers=self.Headers)
				request.get_method = lambda: 'PUT'
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "PUTGET: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def PutPostRequest(self, url, postdata, json=False, xmlrequest=False):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				self.Headers['Content-Length'] = str(len(postdata))
				if json == False:
					self.Headers['Content-Type'] = "application/x-www-form-urlencoded"
				else:
					self.Headers['Content-Type'] = 'application/json'
				request = urllib2.Request(url, headers=self.Headers)
				request.get_method = lambda: 'PUT'
				self.SetupOpener()
				response = self.opener.open(request, postdata, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "PUTPOST: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def DeleteRequest(self, url, xmlrequest=False):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				#self.Headers['Content-Type'] = "application/x-www-form-urlencoded"
				request = urllib2.Request(url, headers=self.Headers)
				request.get_method = lambda: 'DELETE'
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "DELETE: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def MultiPartPostUpload(self, url, postdata, xmlrequest=False):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				if xmlrequest == True:
					self.Headers['X-Requested-With'] = "XMLHttpRequest"
				request = urllib2.Request(url, postdata, headers=self.Headers)
				opener = urllib2.build_opener(MultipartPostHandler,urllib2.HTTPCookieProcessor(self.Jar))
				if self.HandleRedirects == False:
					opener.add_handler(NoRedirection)
				if self.UseProxies == True:
					ph = urllib2.ProxyHandler({'http':self.ProxyData, 'https':self.ProxyData})
					opener.add_handler(ph)
				response = opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "MultipartPostUpload: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def DownloadFile(self, url, thefile):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				request = urllib2.Request(url, headers=self.Headers)
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				with open(thefile, "wb") as local_file:
					local_file.write(response.read())
				local_file.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "DOWNLOAD: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def YUploadFile(self, url, filepath):
		html = ''
		for x in xrange(0, self.Tries):
			try:
				self.ResetHeaders()
				self.Headers['Content-Type'] = "image/jpeg"
				f = open(filepath, "rb")
				image_data = f.read()
				f.close()
				self.Headers['Content-Length'] = str(len(image_data))
				request = urllib2.Request(url, image_data, headers=self.Headers)
				self.SetupOpener()
				response = self.opener.open(request, timeout=self.Timeout)
				self.Location = response.geturl()
				html = response.read()
				if response.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(html)
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
					f.close()
				response.close()
				return html
			except Exception:
				html = ""
				if self.DebugMode: print "YUploadFile: " + url + "\n\n" + traceback.format_exc() + "\n\n"
		return html
	def SafeString(self, inText):
		return urllib.quote(inText, '')
	def ResetHeaders(self):
		if self.KeepAlive:
			self.connection = "keep-alive"
		else:
			self.connection = "close"
		self.Headers = { "User-Agent" : self.UserAgent,
		"Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0." + str(random.randint(1,9)) + ",text/plain;q=0." + str(random.randint(1,9)) + ",text/png,*/*;q=0." + str(random.randint(1,9)),
		"Accept-Language" : "en-us,en;q=0." + str(random.randint(1,9)),
		"Accept-Encoding" : self.AcceptEncoding,
		"Connection" : self.connection }
		if len(self.ExtraHeaders) > 0:
			for h in self.ExtraHeaders:
				if ":" in h:
					name = h[:h.index(":")]
					value = h[h.index(":") + 1:]
					self.Headers[name] = value
	def AddCustomHeader(self, name, value):
		if name != "" or name != None:
			if value !="" or value != None:
				newheader = name + ":" + value
				if not newheader in self.ExtraHeaders:
					self.ExtraHeaders.append(name + ":" + value)
	def ClearCustomHeaders(self):
		if len(self.ExtraHeaders) > 0:
			self.ExtraHeaders = []
	def SetProxy(self, ProxyData):
		self.UseProxies = True
		self.BuiltOpener = False
		self.ProxyData = ProxyData
	def SetUserAgent(self, useragent):
		self.UserAgent = useragent
		self.Headers["User-Agent"] = self.UserAgent
	def ClearCookies(self):
		if len(self.ExtraCookies) > 0:
			self.ExtraCookies = []
		self.BuiltOpener = False
	def AddCookie(self, cookie, domain="", secure=False):
		try:
			cookie = cookie.rstrip()
			cookieName = cookie[:cookie.index("=")]
			cookieValue = cookie[cookie.index("=") + 1:]
			cookieValue = cookieValue[:cookieValue.index(";")]
			cookieDomain = domain
			if domain == "":
				cookieDomain = cookie[cookie.index("domain=") + 7:]
				if ';' in cookieDomain: cookieDomain = cookieDomain[:cookieDomain.index(";")]
			thecookie =  cookielib.Cookie( version=0, name=cookieName,
			value=cookieValue, port=None, port_specified=False,
			domain=cookieDomain, domain_specified=True,
			domain_initial_dot=False, path="/",	path_specified=True,
			secure=secure, expires=None, discard=False, comment=None,
			comment_url=None, rest=None )
			self.ExtraCookies.append(thecookie)
			self.Jar.set_cookie(thecookie)
		except Exception:
			print "\nError adding cookie to the cookie jar.\n"
		return
	def SetupOpener(self):
		# check and build opener for requests...
		if self.BuiltOpener == False:
			self.Jar = cookielib.CookieJar()
			self.Cookies = urllib2.HTTPCookieProcessor(self.Jar)
			self.opener = urllib2.build_opener(self.Cookies)
			if self.HandleRedirects == False:
				self.RedirectHandler = NoRedirection
				self.opener.add_handler(self.RedirectHandler)
			if self.DebugMode == True:
				self.DebugHandler = urllib2.HTTPSHandler(debuglevel=1)
				self.opener.add_handler(urllib2.HTTPSHandler(debuglevel=1))
			if self.UseProxies == True:
				self.ProxyHandler = urllib2.ProxyHandler({'http':self.ProxyData, 'https':self.ProxyData})
				self.opener.add_handler(self.ProxyHandler)
			self.BuiltOpener = True
		return
		
"""

			MultipartPostHandler Class

"""
if six.PY3:
    import io
    import urllib.parse
    import urllib.request
    from email.generator import _make_boundary as choose_boundary
else:
    import cStringIO as io
    from six.moves import urllib
    from mimetools import choose_boundary
doseq = 1
class MultipartPostHandler(urllib.request.BaseHandler):
    # needs to run first
    handler_order = urllib.request.HTTPHandler.handler_order - 10
    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                for(key, value) in list(data.items()):
                    if hasattr(value, 'read'):
                        v_files.append((key, value))
                    else:
                        v_vars.append((key, value))
            except TypeError:
                raise TypeError
            if len(v_files) == 0:
                data = urllib.parse.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if (
                    request.has_header('Content-Type') and
                    request.get_header('Content-Type').find(
                        'multipart/form-data') != 0
                ):
                    six.print_(
                        "Replacing %s with %s" % (
                            request.get_header('content-type'),
                            'multipart/form-data'
                        )
                    )
                request.add_unredirected_header('Content-Type', contenttype)
            request.add_data(data)
        return request
    def multipart_encode(self, v_vars, files, boundary=None, buf=None):
        if six.PY3:
            if boundary is None:
                boundary = choose_boundary()
            if buf is None:
                buf = io.BytesIO()
            for(key, value) in v_vars:
                buf.write(b'--' + boundary.encode("utf-8") + b'\r\n')
                buf.write(b'Content-Disposition: form-data; name="' +
                    key.encode("utf-8") + b'"')
                buf.write(b'\r\n\r\n' + value.encode("utf-8") + b'\r\n')
            for(key, fd) in files:
                try:
                    filename = fd.name.split('/')[-1]
                except AttributeError:
                    filename = 'temp.pdf'
                contenttype = mimetypes.guess_type(filename)[0] or \
                    b'application/octet-stream'
                buf.write(b'--' + boundary.encode("utf-8") + b'\r\n')
                buf.write(b'Content-Disposition: form-data; ' +
                    b'name="' + key.encode("utf-8") + b'"; ' +
                    b'filename="' + filename.encode("utf-8") + b'"\r\n')
                buf.write(b'Content-Type: ' + 
                contenttype.encode("utf-8") + b'\r\n')
                fd.seek(0)
                buf.write(b'\r\n' + fd.read() + b'\r\n')
            buf.write(b'--')
            buf.write(boundary.encode("utf-8"))
            buf.write(b'--\r\n\r\n')
            buf = buf.getvalue()
            return boundary, buf
        else:
            if boundary is None:
                boundary = choose_boundary()
            if buf is None:
                buf = io.StringIO()
            for(key, value) in v_vars:
                buf.write('--%s\r\n' % boundary)
                buf.write('Content-Disposition: form-data; name="%s"' % key)
                buf.write('\r\n\r\n' + value + '\r\n')
            for(key, fd) in files:
                try:
                    filename = fd.name.split('/')[-1]
                except AttributeError:
                    filename = 'temp.pdf'
                contenttype = mimetypes.guess_type(filename)[0] or \
                    'application/octet-stream'
                buf.write('--%s\r\n' % boundary)
                buf.write('Content-Disposition: form-data; \
    name="%s"; filename="%s"\r\n' % (key, filename))
                buf.write('Content-Type: %s\r\n' % contenttype)
                # buffer += 'Content-Length: %s\r\n' % file_size
                fd.seek(0)
                buf.write('\r\n' + fd.read() + '\r\n')
            buf.write('--' + boundary + '--\r\n\r\n')
            buf = buf.getvalue()
            return boundary, buf
    https_request = http_request

def getsize(o_file):
    startpos = o_file.tell()
    o_file.seek(0)
    o_file.seek(0, SEEK_END)
    size = o_file.tell()
    o_file.seek(startpos)
    return size
    
"""

		Handler for when No Redirection is set for HTTP object

"""
class NoRedirection(urllib2.HTTPErrorProcessor):
	# Class for handling no redirection
    def http_response(self, request, response):
        return response
    https_response = http_response  
    
