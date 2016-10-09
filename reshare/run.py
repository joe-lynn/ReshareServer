from application import app
from controllers.resource_binder import bind_resources

if __name__ == '__main__':
	bind_resources()
	app.run(debug=True)

def run_app():
	bind_resources()

print __name__
run_app()
