# TODO(stfinancial): This may just create a mess of dependencies.
from views.listing import bind_views as bl
from views.rental import bind_views as br
from views.user import bind_views as bu

def bind_views():
	bl()
	br()
	bu()

bind_views()
