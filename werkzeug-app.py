from convertor import convert_doc

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

        resp = Response(buf.getvalue())
        resp.content_type = 'application/x-download'
        resp.headers.add('Content-Disposition', 'attachment', filename='converted.odt')
        return resp
    return Response(HTML, content_type='text/html')

if __name__ == '__main__':
    from werkzeug import run_simple
    run_simple('', 5000, application, use_debugger=True, use_reloader=True)
