from application import app
from views.view_binder import bind_views

if __name__ == '__main__':
	bind_views()
	app.run(debug=True)

def run_app():
	bind_views()

print __name__
run_app()
