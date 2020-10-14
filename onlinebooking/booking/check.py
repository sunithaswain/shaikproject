ddd = [{u'dept_date_time': u'2019-02-19T09:09:00', u'arr_date_time': u'2019-02-19T10:59:00', u'train': u'0909', u'arr_station_code': u'7000246', u'arr_time': u'10:59:00', u'dept_station_code': u'7000372', u'arr_station': u'London Victoria', u'dept_station': u'Chichester', u'dept_time': u'09:09:00'}, {u'dept_date_time': u'2019-02-19T10:59:00', u'arr_date_time': u'2019-02-19T11:40:00', u'train': u'1059', u'arr_station_code': u'7000021', u'arr_time': u'11:40:00', u'dept_station_code': u'7000246', u'arr_station': u'London Euston', u'dept_station': u'London Victoria', u'dept_time': u'10:59:00'}, {u'dept_date_time': u'2019-02-19T11:40:00', u'arr_date_time': u'2019-02-19T13:11:00', u'train': u'1140', u'arr_station_code': u'7000096', u'arr_time': u'13:11:00', u'dept_station_code': u'7000021', u'arr_station': u'Crewe', u'dept_station': u'London Euston', u'dept_time': u'11:40:00'}, {u'dept_date_time': u'2019-02-19T13:23:00', u'arr_date_time': u'2019-02-19T13:46:00', u'train': u'1323', u'arr_station_code': u'7000168', u'arr_time': u'13:46:00', u'dept_station_code': u'7000096', u'arr_station': u'Chester', u'dept_station': u'Crewe', u'dept_time': u'13:23:00'}, {u'dept_date_time': u'2019-02-19T14:02:00', u'arr_date_time': u'2019-02-19T14:18:00', u'train': u'1402', u'arr_station_code': u'7023060', u'arr_time': u'14:18:00', u'dept_station_code': u'7000168', u'arr_station': u'Delamere', u'dept_station': u'Chester', u'dept_time': u'14:02:00'}]


print len(ddd)

for i in ddd:
	print i
	print "**"*20

<tr class="a_journey success selected">
                            <td style="width:20%;"><span class="glyphicon glyphicon-chevron-right"></span>{{result.journey_details.0.dept_station}}</td>
                            <td style="width:20%;">{{result.journey_details.0.arr_station}}</td>
                            {% with dep_time=result.departure %}
                            <td style="width:10%;">{{dep_time}}</td>
                            {%endwith%}
                            <td style="width:10%;">{{result.arrival}}</td>
                            <td style="width:10%;">{{result.duration}}</td>
                            <td style="width:10%;">{{result.changes}}</td>
                            {%if result.lowest_price %}
                            <td id = "price_from_{{index_value}}" style="width:10%;" > {{result.lowest_price}} </td>
                            {% else %}
                            <td id = "price_from_{{index_value}}" style="width:10%;" > Details </td>
                            {% endif %}
                          </tr>
