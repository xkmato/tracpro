from __future__ import absolute_import, unicode_literals
from tracpro.unsolicited.views import UnsolicitedCRUDL, ReplyCRUDL

urlpatterns = UnsolicitedCRUDL().as_urlpatterns()
urlpatterns += ReplyCRUDL().as_urlpatterns()

print ReplyCRUDL().as_urlpatterns()