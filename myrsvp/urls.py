from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.signin,name='login'),
    url(r'^regist/$', views.regist,name='regist'),
    url(r'^logout/$',views.signout,name='logout'),
    url(r'^home/$', views.homepage, name='homepage'),
    url(r'^test/$', views.test, name='test'),
    url(r'^error/$', views.wrong, name='wrong'),
    url(r'^succeed/$', views.succeed, name='succeed'),
    #url(r'^myevent/(?P<pk>[0-9]+)/$', views.myevent, name='myevent'),
    url(r'^event/myevent/$', views.myevent, name='myevent'),
    url(r'^event/vendorevent/$', views.vendorevent, name='vendorevent'),
    url(r'^event/guestevent/$', views.guestevent, name='guestevent'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^event/create/$', views.create_event, name='create_event'),
    url(r'^event/(?P<pk>\d+)/eventdelete/$', views.event_delete, name='event_delete'),
    url(r'^event/(?P<pk>\d+)/eventedit/$', views.event_edit, name='event_edit'),
    url(r'^create_question/(?P<pk>[0-9]+)/$', views.create_question, name='create_question'),
    url(r'^create_choice/(?P<event_pk>[0-9]+)/(?P<question_pk>[0-9]+)/$', views.create_choice, name='create_choice'),
    url(r'^question/(?P<pk>\d+)/questiondelete/$', views.question_delete, name='question_delete'),
    url(r'^question/(?P<pk>\d+)/questionedit/$', views.question_edit, name='question_edit'),
    url(r'^event/(?P<event_pk>\d+)/question_detail/(?P<question_pk>\d+)$', views.question_detail, name='question_detail'),
    url(r'^question/(?P<pk>\d+)/vendor_view/$', views.vendor_view, name='vendor_view'),
    url(r'^event/(?P<event_pk>\d+)/rsvp/$', views.rsvp, name='rsvp'),                    
    url(r'^event/(?P<event_pk>\d+)/plusone/$',views.plusone,name='plusone'),
]