# TODO(stfinancial): This may just create a mess of dependencies.
from controllers.listing import bind_resources as bl
from controllers.rental import bind_resources as br
from controllers.user import bind_resources as bu

def bind_resources():
	bl()
	br()
	bu()

