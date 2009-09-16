#!/usr/bin/python
# 2005/04/07
#v1.1.1

# upload.py
# Script and module to allow upload of files
# A refactoring and bugfix of upload.py by Tim Middleton

# Homepage : http://www.voidspace.org.uk/python/recipebook.shtml

# Copyright Michael Foord, 2004 & 2005.
# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/documents/BSD-LICENSE.txt

# For information about bugfixes, updates and support, please join the Pythonutils mailing list.
# http://voidspace.org.uk/mailman/listinfo/pythonutils_voidspace.org.uk
# Comments, suggestions and bug reports welcome.
# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# E-mail fuzzyman@voidspace.org.uk

#######################################################################
# Constants. Used when run as __main__

dirUpload = "../upload"            # directory for upload; will be created if doesn't exist
maxkb = 1000                    # maximum kilobytes to store before no more files accepted
email = "michael@foord.me.uk"     # where to email upload reports;

link = 'http://www.voidspace.org.uk/python/index.shtml'

############################################################
#HTML Templates

HRlink = '<BR><BR><HR><B><A HREF="%s">Home Page</A></B>' % link

formhead = """<html><head>
<title>File Upload</title><body>
<h2>Upload one or more files:</h2>
<P>
There's currently %s %s equalling %.2f kb. """

maxline = "(of a maximum of %s kb allowed) in the upload area.<BR>"

formbody = """
<form action="%s" method="POST" enctype="multipart/form-data">
Name of File 1: <input name="file.1" type="file" size="35"><BR>
Name of File 2: <input name="file.2" type="file" size="35"><BR>
Name of File 3: <input name="file.3" type="file" size="35"><BR>
Name of File 4: <input name="file.4" type="file" size="35"><BR>
Name of File 5: <input name="file.5" type="file" size="35"><BR>
Name of File 6: <input name="file.6" type="file" size="35">
<P><input name="submit" type="submit" value="Upload File(s)">
</form>"""

formfoot = HRlink + "</body></html>"

fullhead = "<HTML><HEAD><TITLE>Upload Aborted</TITLE></HEAD><BODY>"
fullmsg = "There are already %.2f kb files in the upload area, which is more than the %s kb maximum. Therefore your files have not been accepted, sorry."

uploadhead = "<HTML><HEAD><TITLE>Upload Results</TITLE></HEAD><BODY>"

# List of the file 'names' to retrieve from the HTML form.
filelist = ['file.1', 'file.2', 'file.3', 'file.4', 'file.5', 'file.6', ]
serverline = "Content-type: text/html\n"

#######################################################################
# imports

import sys
import os
import glob
import string
import os.path
import cgi
try:
    import cgitb
    cgitb.enable()
except:
    sys.stderr = sys.stdout

try:
    import msvcrt       # we're setting I/O mode to binary on Windows :-)
except ImportError:
    pass
else:
    for fd in(0,1):
        msvcrt.setmode(fd, os.O_BINARY)

#######################################################################
# functions etc

if os.environ.has_key("SCRIPT_NAME"):
    posturl = os.environ["SCRIPT_NAME"]
else:
    posturl = ""

def create_env():
    """Return a list of lines froming the environment variabkes we are emailing."""
    mailENV = ["---------------------------------------\n"]
    for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR','HTTP_FROM','REMOTE_HOST','REMOTE_PORT','SERVER_SOFTWARE','HTTP_REFERER','REMOTE_IDENT','REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
        if os.environ.has_key(x):
            mailENV.append("%s: %s\n" % (x, os.environ[x]))
    mailENV.append("---------------------------------------\n")
    return mailENV

def mailme(msg="", indict=None, **keywargs):
    """This implements the 'email admin' feature.
    It doesn't display any error if this fails."""
    if not indict:
        indict={}
    defaults = {'email' : email, 'from' : email, 'to' : email, 
                   'env' : True, 'subject' : "Upload Report", 'host' : 'localhost'}
    for entry in defaults:
        if not keywargs.has_key(entry):
            keywargs[entry] = indict.get(entry, defaults[entry])
    msg = "Subject: %s\n\n" %  keywargs['subject'] + msg
    if  keywargs['env']:
        for line in create_env():
            msg = msg + line
    try:
        import smtplib
        server = smtplib.SMTP(keywargs['host'])
        server.sendmail(keywargs['email'], [keywargs['to']], msg)
        server.quit()
    except:
        pass        

def getdirsize(indir=dirUpload):
    "Return the size of all the files in a directory."
    if not os.path.exists(dirUpload):
        return 0
    kb=0
    fns = glob.glob(dirUpload+os.sep+"*")
    for x in fns:
        kb = kb + os.stat(x)[6]            
    return kb


def savefiles(data, dirUpload=dirUpload,filelist=filelist, maxkb=maxkb, uploadsize=None):
    """ Given a CGI FieldStorage object, a directory to save to,
    and the list of file keys to check for - this function saves out any uploaded files.
    If necessary it creates the upload directory.

    Returns - (fnList, kbList, kbCount, failed)
    Which is - (list of filenames uploaded and saved, corresponding list of the filesizes, total size of uploaded files,
                list of filenames that failed to upload)
    """
    if uploadsize is None:
        uploadsize=getdirsize()/1024.0
    if not os.path.exists(dirUpload):
        os.mkdir(dirUpload,0777)
    fnList = []
    kbList = []
    kbCount = 0
    failed = []
    for key in filelist:
        if data.has_key(key):
            fn = data[key].filename
            if not fn:
                continue
            if string.rfind(data[key].filename,"\\") >= 0:
                fn = fn[string.rfind(data[key].filename,"\\"):]
            if string.rfind(data[key].filename,"/") >= 0:
                fn = fn[string.rfind(data[key].filename,"/"):]
            if string.rfind(data[key].filename,":") >= 0:
                fn = fn[string.rfind(data[key].filename,":"):]

            if maxkb and (uploadsize+len(data[key].value)/1024.0)>maxkb:
                failed.append(fn)
            else:
                o = open(dirUpload+os.sep+fn,"wb")
                o.write(data[key].value)
                o.close()
                fnList.append(fn)
                kbList.append(len(data[key].value))
                kbCount = kbCount + len(data[key].value)
    return (fnList, kbList , kbCount, failed)

def plural(s,num):
    "Make plural words nicely as possible."
    if num<>1:
        if s[-1] == "s" or s[-1] == "x":
            s = s + "e"
        s = s + "s"
    return s


def has_files(data):
    """Returns 1 if there are any files that are being uploaded.
    Else it returns 0."""
    anyfiles = 0
    for entry in filelist:
        if data.has_key(entry):
            anyfiles = 1
            break
    return anyfiles

def do_upload(data, fns, uploadsize):
    """Do the upload and print any message."""
    fnList, kbList , kbCount, failed = savefiles(data)
    print uploadhead
    if len(fnList):
        msg = "<H2>%s %s totalling %.2f kb uploaded successfully:</H2>\n\n" % (len(fnList),plural("file",len(fnList)),kbCount / 1024.0)        
        print msg
        print "<HR><P><UL>"
        for x in range(0,len(fnList)):
            msg = msg + "  * %s (%.2f kb)\n" % (fnList[x],kbList[x] / 1024.0)
            print "<LI>%s (%.2f kb)" % (fnList[x],kbList[x] / 1024.0)
        print "</UL>"
        print "<P><HR>"
    if failed:
        newmess = 'The following files failed to upload as the max size was reached :'
        msg = msg + '\n' + newmess + '\n'
        print "<P>%s<BR><UL>" % newmess
        for entry in failed:
            print '<LI>' + entry 
            msg = msg + entry + '\n'
        print '</UL><<BR>><HR><P>'
    print "Now a total of %.2f kb in %s %s in the upload area.<BR>" % (uploadsize + (kbCount / 1024.0),len(fnList)+fns,plural("file",len(fnList)+fns))
    if email:
        mailme(msg[4:]+"\n\n")
    if not len(fnList):
        print "No files were successfully uploaded.<BR>"
    print formfoot

#######################################################################
# If run as a cgi this part performs the upload

def main():
    print serverline
    data = cgi.FieldStorage()
    anyfiles = has_files(data)
    
    uploadsize = getdirsize()/1024.0            # the current directory size in kb
    fns = len(glob.glob(dirUpload+os.sep+"*"))   # no of files in the directory
    if anyfiles and (not maxkb or uploadsize < maxkb):    # we are uploading
        do_upload(data, fns, uploadsize)
    elif maxkb and uploadsize >= maxkb:
        print fullhead
        print fullmsg % (uploadsize, maxkb)
        print formfoot
    else:
        print formhead % (fns, plural('file', fns), uploadsize)
        if maxkb: print maxline % maxkb
        print formbody % posturl
        print formfoot

#######################################################################
if __name__ == '__main__':
    main()

"""
TODO/ISSUES
HTML templates in a separate file.
Allow protocol for splitter - uploading files bigger than 1mb in pieces and rejoining.
Add the directory display and editing features - file management, of which this is a part.
Allow for keeping directory structure - say from a zipfile.
(I.E. develop into a CGI file manager script)


CHANGELOG
2005/04/07      Version 1.1.1
We now set I/O to binary mode for windows.

02-10-04        Version 1.1.0
Switched to smtplib rather than sendmail.
Created 'main()'.
Another refactoring.

03-07-04        Version 1.0.0
Refactored the excellent  upload.py by Tim Middleton
(Including fixing a couple of bugs in it.)
"""
