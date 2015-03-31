from __future__ import absolute_import, unicode_literals
from tracpro.unsolicited.views import UnsolicitedCRUDL

urlpatterns = UnsolicitedCRUDL().as_urlpatterns()