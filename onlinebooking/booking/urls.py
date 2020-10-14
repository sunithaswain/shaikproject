from django.conf.urls import url
# import onlinebooking.booking.views as views
from . views import *
urlpatterns = [
    url(r'^home/', allview, name='homedetail'),
    url(r'^ticket/', ticket_view, name='ticket'),
    url(r'^traveller_info/', traveller_info, name='traveller'),
    url(r'^checkinfo/',checkinfodeatil,name='check'),
    url(r'^summarydet/',summarydetail,name='sumaryinfo'),
    url(r'^summary1deta/',summary1deta,name='summary1info'),
    url(r'^pointtest/', pointdet,name='pointtail'),
    # url(r'^home2/', allviewtest1, name='homedetail2'),
    url(r'^ticket1/', ticket_view1, name='tickettest1'),
 ] 