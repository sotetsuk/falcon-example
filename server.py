import json
import falcon


class Middleware(object):
    def process_request(self, req, resp):
        print "process_request called"

    def process_resource(self, req, resp, resource, param):
        print "process_resource called", resource, param

    def process_response(self, req, resp, resource):
        print "process_response called", resource


def before(before_param):
    def hook(req, resp, resource, params):
        print "before called", resource

    return hook


def after(after_param):
    def hook(req, resp, resource):
        print "after called", resource

    return hook


class CommentsResource(object):

    @falcon.before(before("get beofre param"))
    @falcon.after(after("get after param"))
    def on_get(self, req, resp):
        comments = self._get_comments()
        resp.body = json.dumps(comments)
	resp.set_header('Cache-Control', 'no-cache')
	resp.set_header('Access-Control-Allow-Origin', '*')

    @falcon.before(before("post before param"))
    @falcon.after(after("post after param"))
    def on_post(self, req, resp):
        comments = self._get_comments()
        body = req.stream.read()
        print(body)
        new_comments = json.loads(body)
        comments.append(new_comments)
        self._write_comments(comments)

    def _get_comments(self):
        with open('comments.json', 'r') as f:
            comments = json.loads(f.read())

        return comments

    def _write_comments(self, comments):
        with open('comments.json', 'w') as f:
            f.write(json.dumps(comments, indent=4, separators=(',', ': ')))


app = falcon.API(middleware=Middleware())
app.add_route("/api/comments", CommentsResource())


if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("127.0.0.1", 3001, app)
    httpd.serve_forever()
