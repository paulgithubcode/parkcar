from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'parkcar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^cekjumlah/', 'parkapp.views.number_of_parked_cars'),
    url(r'^park/', 'parkapp.views.park'),
    url(r'^unpark/', 'parkapp.views.unpark'),
    url(r'^get_car_information/', 'parkapp.views.get_car_information'),
    url(r'^get_slot_information/', 'parkapp.views.get_slot_information'),
]
