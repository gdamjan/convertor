from convertor import convert_doc

from webob.dec import wsgify
from webob import Response

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


@wsgify
def application(req):
    if req.method == 'POST':
        file_in = req.POST['myfile']
        buf = convert_doc(file_in.file)

        filename = file_in.filename.replace('.odt', '-converted.odt')
        resp = Response(buf.getvalue())
        resp.content_type = 'application/x-download'
        resp.content_disposition = 'attachment; filename=%s' % filename
        return resp
    return Response(HTML, content_type='text/html')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 5000, application).serve_forever()
