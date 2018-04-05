from .core import convert_doc

from werkzeug import Request, Response

HTML = '''\
<HTML>
<HEAD>
 <TITLE>test</TITLE>
</HEAD>
<BODY>
    <form action="" method="post" enctype="multipart/form-data">
       <input id="myfile" type="file" name="myfile">
       <input type="submit" value="Go!">
    </form>
</BODY>
</HTML>
'''

@Request.application
def application(req):
    if req.method == 'POST':
        file_in = req.files['myfile']
        buf = convert_doc(file_in)

        filename = file_in.filename.replace('.odt', '-converted.odt')
        resp = Response(buf.getvalue())
        resp.content_type = 'application/x-download'
        resp.headers.add('Content-Disposition', 'attachment', filename=filename)
        return resp
    return Response(HTML, content_type='text/html')
