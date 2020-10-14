# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import xmltodict
import json
import ast
from datetime import datetime
from xlrd import open_workbook
import os, sys
from django.conf import settings
from django.shortcuts import redirect
from .models import Cart, CartProducts, CartProductPassengers, CartProductDetails
from djmoney.money import Money
import pickle, uuid
# import pandas as pd

# import onlinebooking.settings

############## logging ###################

# importing module
import logging
from logdna import LogDNAHandler

options = {
    'hostname': 'desktop',
    'ip': '10.0.0.5',
    'mac': 'C0:FF:EE:C0:FF:EE'
}

options['index_meta'] = True

# Creating an object
logger = logging.getLogger('logdna')

logger.setLevel(logging.INFO)

test = LogDNAHandler(settings.LOGDNA_INGEST_KEY, options)
# #print settings.LOGDNA_INGEST_KEY
# #print test
# log.addHandler(test)

# log.warn("Warning message", {'app': 'bloop'})
# log.info("Info message")

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


##########

# Create your views here.
def allview(request):
    """
    This view to collect all details from Home Page
    """

    if request.method == "POST":

        if request.session.get('sessionid') is None:
            uuid_id = str(uuid.uuid4())
            request.session['sessionid'] = uuid_id
        else:
            session_id = request.session.get('sessionid')

        originStattion = request.POST.get('txtfromstation')
        destStattion = request.POST.get('txttostation')
        departureDate = request.POST.get('txtfromdate')
        departureTime = request.POST.get('Ddldeptime')
        returnDate = request.POST.get('txttodate')
        returnTime = request.POST.get('DdlReturntime')
        numAdults = request.POST.get('DdlAdults')
        numChilds = request.POST.get('DdlNonAdults')
        childAges = json.loads(request.POST.get('childAges'))

        date_string = str(departureDate)
        format1 = "%d-%b-%Y"
        format2 = "%Y-%m-%d"
        actual_date = datetime.strptime(date_string, format1).strftime(format2)

        request.session['origin'] = str(originStattion)
        request.session['destination'] = str(destStattion)
        request.session['deptDate'] = str(actual_date)
        request.session['deptTime'] = str(departureTime)
        request.session['adults'] = int(numAdults)
        request.session['children'] = int(numChilds)
        request.session['child_ages'] = childAges
        request.session.modified = True
        # print request.session['deptDate'] , "+++++"
        return HttpResponseRedirect('/alltest/ticket/')
    else:
        session_id = request.session.get('sessionid')
        request.session['sessionid'] = session_id
        request.session.modified = True
        return render(request, "booking/index.html", {})

# def allview(request):
#     """
#     This view to collect all details from Home Page
#     """
#     if request.method == "POST":
#         originStattion = request.POST.get('txtfromstation')
#         destStattion = request.POST.get('txttostation')
#         departureDate = request.POST.get('txtfromdate')
#         departureTime = request.POST.get('Ddldeptime')
#         returnDate = request.POST.get('txttodate')
#         returnTime = request.POST.get('DdlReturntime')
#         numAdults = request.POST.get('DdlAdults')
#         numChilds = request.POST.get('DdlNonAdults')
#
#         date_string = str(departureDate)
#         format1 = "%d-%b-%Y"
#         format2 = "%Y-%m-%d"
#         actual_date = datetime.strptime(date_string, format1).strftime(format2)
#
#         request.session['origin'] = str(originStattion)
#         request.session['destination'] = str(destStattion)
#         request.session['deptDate'] = str(actual_date)
#         request.session['deptTime'] = str(departureTime)
#         request.session['adults'] = int(numAdults)
#         request.session['children'] = int(numChilds)
#         return HttpResponseRedirect('/alltest/ticket/')
#     else:
#         return render(request, "booking/index.html", {})


def ticket_view(request):
    """
    Point To Point Tickets generating view
    """

    if request.method == "POST":
        session_id = request.session.get('sessionid')
        request.session.modified = True
        ''' fare '''
        fare = request.POST.get('fare', False)
        print (fare,"fffffffffff")
        if fare:
            print (fare,"nnnnnnnnnnn")
            request.session['fare'] = fare
        ''' fare class'''
        fare_class = request.POST.get('fareclass', False)
        if fare_class:
            request.session['fare_class'] = fare_class
        ''' fare reference '''
        fare_ref = request.POST.get('farereference', False)
        if fare_ref:
            request.session['fare_ref'] = fare_ref
        ''' heading '''
        heading = request.POST.get('header', False)
        if heading:
            request.session['heading'] = heading
        ''' adults '''
        no_of_adults = request.POST.get('adults_count', False)
        if no_of_adults:
            request.session['adult_count'] = no_of_adults
        ''' childs'''
        no_of_childs = request.POST.get('child_count', False)
        if no_of_childs:
            request.session['child_count'] = no_of_childs

        passport = nationality = dob = countryResidence = birthPlace = age = ""
        checkingData = request.session.get('resultData')
        if checkingData:
            passport = str(checkingData[0][0]['is_passport'])
            nationality = str(checkingData[0][0]['is_nationality'])
            dob = str(checkingData[0][0]['is_dob'])
            countryResidence = str(checkingData[0][0]['is_cntryres'])
            birthPlace = str(checkingData[0][0]['is_birthplace'])
            if checkingData[0][0].get('is_age'):
                age = str(checkingData[0][0]['is_age'])

            request.session['passport'] = passport
            request.session['nationality'] = nationality
            request.session['dob'] = dob
            request.session['countryResidence'] = countryResidence
            request.session['birthPlace'] = birthPlace
            request.session['age'] = age

        request.session['sessionid'] = session_id
        request.session.modified = True

        return HttpResponseRedirect('/alltest/traveller_info')
    else:
        session_id = request.session.get('sessionid')
        ErroMessage = ""
        originLoc = request.session['origin']
        destinationLoc = request.session['destination']
        date_string = request.session['deptDate'] + "T" + request.session['deptTime']
        date_time_obj = datetime.strptime(request.session['deptDate'], '%Y-%m-%d')
        display_date = date_time_obj.date()
        no_of_adults = request.session['adults']
        no_of_childs = request.session['children']
        child_ages = request.session.get('child_ages')
        ReturnReturnDate = ""
        wb = open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
        worksheet = wb.sheet_by_index(0)
        nc = worksheet.ncols
        nr = worksheet.nrows
        ortakes = []
        desttakes = []
        fr = []
        orgLocCode = 0
        countryCode = 0
        destLocCode = 0
        for cr in range(1, nr):
            firstcol = worksheet.cell_value(cr, 1).encode('utf-8')
            if firstcol == originLoc:
                orgLocCode = int(worksheet.cell_value(cr, 0))
                countryCode = int(worksheet.cell_value(cr, 2))
            if firstcol == destinationLoc:
                destLocCode = int(worksheet.cell_value(cr, 0))
                countryCode = int(worksheet.cell_value(cr, 2))

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        root = ET.Element("ACP_RailAvailRQ", xmlns="http://www.acprailinternational.com/API/R2",
                          ResponseType="Native-Availability")
        pos = ET.SubElement(root, "POS")
        requestor = ET.SubElement(pos, "RequestorID").text = "RTG-XML"
        rail_avail_info = ET.SubElement(root, "RailAvailInfo")
        origins = ET.SubElement(rail_avail_info, 'OriginDestinationSpecifications')
        origin1 = ET.SubElement(origins, 'OriginLocation', LocationCode="{0}".format(orgLocCode))
        origin2 = ET.SubElement(origins, 'DestinationLocation', LocationCode="{0}".format(destLocCode))
        origin3 = ET.SubElement(origins, 'Departure', DepartureDate="{0}".format(date_string))
        if ReturnReturnDate:
            origin4 = ET.SubElement(origins, 'Return', ReturnDate="{0}".format(""))

        passengers = ET.SubElement(rail_avail_info, 'PassengerSpecifications')
        # for adults
        passtype = ET.SubElement(passengers, 'PassengerType', Age="-1", Quantity="{0}".format(no_of_adults))
        # for childs
        if child_ages:
            for i in child_ages:
                passtype = ET.SubElement(passengers, 'PassengerType', Age=str(i), Quantity="1")
        fare_qual = ET.SubElement(rail_avail_info, 'FareQualifier RateCategory="Regular"')
        responsePt = ET.SubElement(rail_avail_info, 'ResponsePtPTypes')
        responsePt1 = ET.SubElement(responsePt, 'ResponsePtPType').text = "TW"
        mydata = ET.tostring(root)
        #print(mydata)
        #print("*******" * 15)
        # xml_data += mydata(it supports in python 2)
        xml_data += mydata.decode('utf-8') #(for python 3)
        print(xml_data)
        print("==================" * 15)

        serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
        headers = {'content-type': 'application/xml; charset=utf-8'}
        # print "Before request"
        Result = requests.post(serURL, data=xml_data, headers=headers)
        #print(Result)
        #print(">>>>>>>" * 15)
        if Result.status_code == 200:
            response = Result.text
            print(response,"(((((((((((((((((((((((")
            result = xmltodict.parse(response)

            print(result)

            try:
                result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))
                result = result.encode('utf-8')
                #print("*******"*15)
                #print(result)
            except:
                pass

            if result['ACP_RailAvailRS'].get('OriginDestinationOptions') is not None:

                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get(
                        'OriginLocation') is not None:
                    originLocation = \
                    result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation'][
                        '@Name']
                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get(
                        'DestinationLocation') is not None:
                    destinationLocation = \
                    result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'][
                        'DestinationLocation']['@Name']
                journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys'][
                    'Journey']

                result_list = []
                fareRPHS_List = []

                for index, i in enumerate(journey):
                    result_dict = {}
                    changes = i['JourneySegments']['JourneySegment']
                    if i.get('FareRPHs'):
                        fareRPHS_List.append(i['FareRPHs']['FareRPH'])
                        result_dict['fareRPHS_List'] = i['FareRPHs']['FareRPH']
                    result_dict['changes'] = len(changes) - 1

                    deptTimeList = []
                    arrivalTimeList = []
                    journeyDetailsList = []
                    if len(changes) == 1:
                        segment = changes['TrainSegment']
                        trainNum = segment['@TrainNumber']
                        departDateTime = segment['@DepartureDateTime']
                        arrivalDateTime = segment['@ArrivalDateTime']
                        departStation = segment['DepartureStation']
                        departStationName = departStation['@Name']
                        departStationCode = departStation['@LocationCode']
                        arrivaltStation = segment['ArrivalStation']
                        arrivaltStationName = arrivaltStation['@Name']
                        arrivaltStationCode = arrivaltStation['@LocationCode']

                        depttime = departDateTime.split("T")[-1]
                        deptTimeList.append(depttime)
                        arrtime = arrivalDateTime.split("T")[-1]
                        arrivalTimeList.append(arrtime)

                        journeyDetails = {}
                        journeyDetails['train'] = str(trainNum)
                        journeyDetails['dept_station'] = str(departStationName)
                        journeyDetails['dept_station_code'] = str(departStationCode)
                        journeyDetails['dept_time'] = str(depttime)
                        journeyDetails['arr_station'] = str(arrivaltStationName)
                        journeyDetails['arr_station_code'] = str(arrivaltStationCode)
                        journeyDetails['arr_time'] = str(arrtime)
                        journeyDetails['dept_date_time'] = str(departDateTime)
                        journeyDetails['arr_date_time'] = str(arrivalDateTime)

                        journeyDetailsList.append(journeyDetails)
                    else:
                        for change in changes:
                            segment = change['TrainSegment']
                            trainNum = segment['@TrainNumber']
                            departDateTime = segment['@DepartureDateTime']
                            arrivalDateTime = segment['@ArrivalDateTime']
                            departStation = segment['DepartureStation']
                            departStationName = departStation['@Name']
                            departStationCode = departStation['@LocationCode']
                            arrivaltStation = segment['ArrivalStation']
                            arrivaltStationName = arrivaltStation['@Name']
                            arrivaltStationCode = arrivaltStation['@LocationCode']

                            depttime = departDateTime.split("T")[-1]
                            deptTimeList.append(depttime)
                            arrtime = arrivalDateTime.split("T")[-1]
                            arrivalTimeList.append(arrtime)

                            journeyDetails = {}
                            journeyDetails['train'] = str(trainNum)
                            journeyDetails['dept_station'] = str(departStationName)
                            journeyDetails['dept_station_code'] = str(departStationCode)
                            journeyDetails['dept_time'] = str(depttime)
                            journeyDetails['arr_station'] = str(arrivaltStationName)
                            journeyDetails['arr_station_code'] = str(arrivaltStationCode)
                            journeyDetails['arr_time'] = str(arrtime)
                            journeyDetails['dept_date_time'] = str(departDateTime)
                            journeyDetails['arr_date_time'] = str(arrivalDateTime)
                            journeyDetailsList.append(journeyDetails)

                    result_dict['departure'] = deptTimeList[0]
                    result_dict['arrival'] = arrivalTimeList[-1]
                    datetimeFormat = '%H:%M:%S'
                    timeDuration = datetime.strptime(str(result_dict['arrival']), datetimeFormat) \
                                   - datetime.strptime(str(result_dict['departure']), datetimeFormat)

                    result_dict['duration'] = str(timeDuration)
                    result_dict['journey_details'] = journeyDetailsList
                    result_dict['index'] = index
                    result_list.append(result_dict)

                request.session['response_result'] = result_list
                if result['ACP_RailAvailRS'].get('Fares') is not None:
                    fares = result['ACP_RailAvailRS']['Fares']['Fare']
                    sample = []
                    fare_classes_list = []

                    for ff in fareRPHS_List:
                        li = []
                        for j in fares:
                            clas = j['@Class']
                            if clas.__contains__('-'):
                                clas = clas.split("-")[-1]
                            fare_classes_list.append(clas)
                            if len(ff) != 0:
                                for k in ff:
                                    if k == j['@FareReference']:
                                        dic1 = {}
                                        dic1['total_price'] = j['TotalPrice']['@Amount']
                                        dic1['fareRefer'] = j['@FareReference']
                                        dic1['class'] = clas
                                        dic1[clas] = j['TotalPrice']['@Amount']
                                        dic1['product_name'] = str(j['ProdMarketingName']).split(">")[1].replace(
                                            "</div", "")
                                        dic1['sales_condition'] = j['SalesConditions']['@RefundPolicy']
                                        dic1['ticket_option'] = j['@TicketOption']
                                        dic1['is_passport'] = j['@PassportRequired']
                                        dic1['is_dob'] = j['@DateOfBirthRequired']
                                        dic1['is_paxname'] = j['@PaxNameRequested']
                                        dic1['is_cntryres'] = j['@CntryResidenceRequired']
                                        dic1['is_nationality'] = j['@NationalityRequired']
                                        dic1['is_birthplace'] = j['@PlaceOfBirthRequired']
                                        dic1['is_email'] = j['@EmailRequired']
                                        if j['PassengerTypePrices'].get('MixDetails'):
                                            dic1['is_age'] = \
                                            j['PassengerTypePrices']['MixDetails']['PassengerPlaceholder'][0]['@Age']
                                        li.append(dic1)
                            else:
                                li = []
                                ff == j['@FareReference']
                                dic1 = {}
                                dic1['total_price'] = j['TotalPrice']['@Amount']
                                dic1['fareRefer'] = j['@FareReference']
                                dic1['class'] = clas
                                dic1['product_name'] = str(j['ProdMarketingName']).split(">")[1].replace("</div", "")
                                dic1['sales_condition'] = j['SalesConditions']['@RefundPolicy']
                                dic1['ticket_option'] = j['@TicketOption']
                                dic1['is_passport'] = j['@PassportRequired']
                                dic1['is_dob'] = j['@DateOfBirthRequired']
                                dic1['is_paxname'] = j['@PaxNameRequested']
                                dic1['is_cntryres'] = j['@CntryResidenceRequired']
                                dic1['is_nationality'] = j['@NationalityRequired']
                                dic1['is_birthplace'] = j['@PlaceOfBirthRequired']
                                dic1['is_email'] = j['@EmailRequired']
                                if j['PassengerTypePrices'].get('MixDetails'):
                                    dic1['is_age'] = j['PassengerTypePrices']['MixDetails']['PassengerPlaceholder'][0][
                                        '@Age']
                                li.append(dic1)
                                sample.append(li)
                        sample.append(li)
                    fare_classes_list = list(set(fare_classes_list))

                    # print sample
                    # print "#######"

                    final_list = []
                    dd = {}
                    ddd = {}
                    fare_ref_list = []
                    f_d = {}
                    f_dd = {}
                    for main_index, i in enumerate(sample):
                        min_value = 0
                        min_value_list = []
                        sales = ''
                        for kk in i:
                            if kk['product_name'] not in dd:
                                for index, class1 in enumerate(fare_classes_list):
                                    if kk.get(class1) is not None:
                                        list1 = {}
                                        list1[class1] = kk[class1]
                                        list1[kk[class1]] = kk['fareRefer']
                                        dd[kk['product_name']] = list1

                                        list2 = {}
                                        list2[class1] = kk['fareRefer']
                                        f_d[kk['product_name']] = list2
                                        if min_value == 0:
                                            min_value = kk[class1]
                                            min_value_list.append(min_value)

                                        elif min_value > kk[class1]:
                                            min_value = kk[class1]
                                            min_value_list.append(min_value)


                            else:

                                for index, class1 in enumerate(fare_classes_list):
                                    if kk.get(class1) is not None:
                                        name = dd.get(kk['product_name'])
                                        name[class1] = kk[class1]
                                        name[kk[class1]] = kk['fareRefer']
                                        dd[kk['product_name']] = name

                                        name1 = f_d.get(kk['product_name'])
                                        name1[class1] = kk['fareRefer']
                                        f_d[kk['product_name']] = name1

                                        if min_value == 0:
                                            min_value = kk[class1]
                                            min_value_list.append(min_value)

                                        elif min_value > kk[class1]:
                                            min_value = kk[class1]
                                            min_value_list.append(min_value)
                            sales = kk['sales_condition']

                        min_value_list = sorted([float(i) for i in min_value_list])
                        min_value = min(min_value_list)
                        dd['min'] = min_value
                        dd['sales'] = str(sales)
                        ddd[main_index] = dd
                        f_dd[main_index] = f_d

                        if result_list[main_index]['index'] == main_index:
                            result_list[main_index]['lowest_price'] = min_value

                        final_list.append(ddd)
                        fare_ref_list.append(f_dd)
                        # print final_list
                        # print "$$"*20
                        # print fare_ref_list

                        dd = {}
                        ddd = {}
                        f_d = {}
                        f_dd = {}

                    # print "After successfull response"
                    request.session['resultData'] = sample
                    request.session['sessionid'] = session_id
                    request.session.modified = True
                    return render(request, "booking/tickets.html",
                                  {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                                   "final_result": result_list, "prices_data": sample, 'classes': fare_classes_list,
                                   'result_output': final_list, 'fare_refs': fare_ref_list, 'adults': no_of_adults,
                                   'childs': no_of_childs, "Error": ErroMessage})


                else:
                    return render(request, "booking/tickets.html",
                                  {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                                   "final_result": result_list, "prices_data": [], 'classes': [],
                                   'result_output': [], 'adults': no_of_adults, 'childs': no_of_childs,
                                   "Error": ErroMessage})
            else:
                ErroMessage = "Getting Web Service Error"
                # response = LogDNAHandler(settings.LOGDNA_INGEST_KEY, Result)
                # logger.addHandler(response)
                logger.info("Fares are not Available for trains")
                # logger.debug("Fares are not Available for trains")

                return render(request, "booking/tickets.html",
                              {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                               "Error": ErroMessage})
        else:
            ErroMessage = "No Response"
            # response = LogDNAHandler(settings.LOGDNA_INGEST_KEY, Result)
            # logger.addHandler(response)
            logger.info("Fares are not Available for trains")
            # logger.debug("Response is not Available from API")
            return render(request, "booking/tickets.html",
                          {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date, "Error": ErroMessage})


def traveller_info(request):
    '''
    Passengers Page view
    '''
    if request.method == "POST":
        session_id = request.session.get('sessionid')
        adult_count = child_count = fare = fare_class = fare_ref = ''
        if request.session:
            fare_class = request.session.get('fare_class')
            if fare_class:
                request.session['fare_class'] = fare_class
            fare_ref = request.session.get('fare_ref')
            if fare_ref:
                request.session['fare_ref'] = fare_ref
            fare = request.session.get('fare')
            if fare:
                request.session['fare'] = fare
            adult_count = request.session.get('adult_count')
            if adult_count:
                request.session['adult_count'] = adult_count
            child_count = request.session.get('child_count')
            if adult_count:
                request.session['child_count'] = child_count

        passengers_info = json.loads(request.POST.get('passengersData'))
        passengers_num = int(adult_count) + int(child_count)
        my_list = passengers_info[2:]
        my_list = my_list[:len(my_list) - 4]

        n = len(my_list) / passengers_num

        if n != 0:
            final_passengers_list = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n)]
        else:
            final_passengers_list = my_list

        passengers_data = []
        for i in final_passengers_list:
            del i[0]
            passengers_data.append(i)

        # To display Cart Product details function
        cart_prod_details = getCartProductDetails(request, int(fare_ref))
        data_from_models = cartModelsDataCreation(request, fare, fare_class, passengers_num, cart_prod_details[1],
                                                  passengers=passengers_data)
        # data_from_models = [CartProductDetails.objects.all()]
        trainNumber = deptStation = deptTime = arrStation = arrTime = ''
        trainCategory = fare_class
        productDetails = data_from_models[0]
        pro = []
        for i in productDetails:
            l = []
            dict1 = {}
            dict1['train'] = i.train
            dict1['departure_date'] = str(i.departure_date)
            dict1['arrival_date'] = str(i.arrival_date)
            dict1['from_station'] = i.from_station
            dict1['to_station'] = i.to_station
            dict1['train_category'] = i.train_category
            dict1['netprice'] = str(i.netprice)
            dict1['passengers_num'] = i.passengers_num
            dict1['id'] = i.id
            l.append(dict1)
            pro.append(l)

        request.session['cart_products'] = pro
        request.session['passengers_Data'] = passengers_data
        request.session['passengers_num'] = passengers_num
        request.session['sessionid'] = session_id
        request.session.modified = True
        return HttpResponseRedirect('/alltest/checkinfo')
    else:
        session_id = request.session.get('sessionid')
        heading = no_of_adults = passport = no_of_childs = nationality = dob = countryResidence = birthPlace = age = ""

        if request.session:
            heading = request.session['heading']
            no_of_adults = range(int(request.session['adult_count']))
            no_of_childs = range(int(request.session['child_count']))
            passport = request.session.get('passport')
            nationality = request.session.get('nationality')
            dob = request.session.get('dob')
            countryResidence = request.session.get('countryResidence')
            birthPlace = request.session.get('birthPlace')
            age = request.session.get('age')

        request.session['sessionid'] = session_id
        request.session.modified = True

        return render(request, "booking/traveller-information.html",
                      {'adults_count': no_of_adults, 'child_count': no_of_childs,
                       'date_text': heading, 'passport': passport, 'dob': dob, 'nationality': nationality,
                       'country_residence': countryResidence, 'birth_place': birthPlace})


def getCartProductDetails(request, ref):
    """
        Cart Product Details Data (For displaying purpose only)
    """

    session_id = request.session.get('sessionid')
    result_list_data = request.session['response_result']

    dic = {}
    dic1 = {}
    for i in result_list_data:
        for j1, j2 in i.items():
            if j1 == 'fareRPHS_List':
                j2 = [int(x.encode('utf-8')) for x in j2]
                if ref in j2:
                    dic[ref] = i['journey_details']
                else:
                    pass
        dic1['multiple_segments'] = i['journey_details']

    data = {}

    if ref in dic:
        for i in dic[ref]:
            data = i
    return [data, dic1]


def checkinfodeatil(request):
    '''
    Cart Page view
    '''
    if request.method == "POST":
        session_id = request.session.get('sessionid')
        if request.POST.get('removeCart'):
            remove_cart_id = request.POST.get('removeCart').encode('utf-8')
            delete_item = CartProductDetails.objects.get(id=remove_cart_id)

            cartProductId = delete_item.cart_product_id

            # passengers model data removal
            CartProductPassengers.objects.filter(cart_product_id=cartProductId).delete()
            # cart product  details model data removal
            CartProductDetails.objects.filter(id=remove_cart_id).delete()
            # cart product  details model data removal
            CartProducts.objects.filter(id=cartProductId).delete()
            productDetails = CartProductDetails.objects.all()

            pro = []
            for i in productDetails:
                l = []
                dict1 = {}
                dict1['train'] = i.train
                dict1['departure_date'] = str(i.departure_date)
                dict1['arrival_date'] = str(i.arrival_date)
                dict1['from_station'] = i.from_station
                dict1['to_station'] = i.to_station
                dict1['train_category'] = i.train_category
                dict1['netprice'] = str(i.netprice)
                dict1['passengers_num'] = i.passengers_num
                dict1['id'] = int(i.id)

                l.append(dict1)
                pro.append(l)

            request.session['cart_products'] = pro
            request.session.modified = True
            return HttpResponseRedirect("/alltest/checkinfo")
        else:
            return HttpResponseRedirect("/alltest/checkinfo")



    else:

        session_id = request.session.get('sessionid')

        fare = fare_ref = passengers = passengers_num = fare_class = ''
        trainNumber = deptStation = deptTime = arrStation = arrTime = productDetails = ''

        if request.session:
            fare = request.session.get('fare')
            fare_ref = request.session.get('fare_ref')
            passengers_data = request.session.get('passengers_Data')
            passengers_num = request.session.get('passengers_num')
            fare_class = request.session.get('fare_class')

            trainNumber = request.session.get('train')
            deptStation = request.session.get('deptStation')
            deptTime = request.session.get('deptTime')
            arrStation = request.session.get('arrStation')
            arrTime = request.session.get('arrTime')
            trainCategory = request.session.get('trainCategory')
            productDetails = request.session.get('cart_products')

        request.session['sessionid'] = session_id

        request.session.modified = True

        return render(request, 'booking/checkout.html', {'cartDetails': 'cart_prod_details',
                                                         'Train': trainNumber, 'DeptStation': deptStation,
                                                         'DeptTime': deptTime,
                                                         'ArrStation': arrStation, 'ArrTime': arrTime,
                                                         "passengercount": passengers_num,
                                                         "faredata": fare, 'fareClass': trainCategory,
                                                         'cartProducts': productDetails})


def cartModelsDataCreation(request, fare, fare_class, passengers_num, prodDetails, passengers=[]):
    """
        Cart related models data insertion
    """

    #  Cart Creation
    # request.session.modified = True
    # #print "model creation views"
    from_station = to_station = dept_date = ""
    session_id = request.session.get('sessionid')
    if request.session.get('origin'):
        from_station = request.session.get('origin')
    if request.session.get('destination'):
        to_station = request.session.get('destination')
    product_name = str(from_station) + "-" + str(to_station)
    if request.session.get('deptDate'):
        dept_date = request.session.get('deptDate')
        # dept_date = datetime(dept_date).date()

    # #print session_id

    # #print passengers
    for i, j in enumerate(passengers):
        dict1 = {}
        n = []
        for e in j:
            dict1.update(e)
        n.append(dict1)
        passengers[i] = n

    for index, i in enumerate(passengers):
        ll = []
        dict1 = {}
        for j in i:
            if j.get('first_name'):
                dict1.update(j)
            else:
                dict1.update({'first_name': 'false'})
            if j.get('passport'):
                dict1.update(j)
            else:
                dict1.update({'passport': 'false'})
            if j.get('secondname'):
                dict1.update(j)
            else:
                dict1.update({'secondname': 'false'})
            if j.get('nationality'):
                dict1.update(j)
            else:
                dict1.update({'nationality': 'false'})
            if j.get('dob'):
                dict1.update(j)
            else:
                dict1.update({'dob': 'false'})
            if j.get('age'):
                dict1.update(int(j))
            else:
                dict1.update({'age': -1})
        ll.append(dict1)
        passengers[index] = ll
    # #print passengers

    ##################################################################
    # New code for inserting data into db
    ##################################################################

    # Cart model data insertion
    addCart = Cart.objects.create(sessionId=session_id, created_date=datetime.now(), booking_ref='',
                                  user_id=124, agent_ref='rail booking', notes='adding  cart', status=0,
                                  currency_id=0, netprice=Money(fare, 'USD'))

    # Cart Product model data insertion
    cartProduct = CartProducts.objects.create(
        cart_id=addCart.id, service=str(fare_class), product_name=product_name, product_id=1,
        status=0, netprice=Money(fare, 'USD'), passengers_num=int(passengers_num),
        start_date=dept_date, Rule='Non-Refundable', fare=Money(fare, 'USD'), settlementprice=Money(fare, 'USD'))

    # Cart Product Details model data insertion

    prod_detailsList = []

    for detail in prodDetails['multiple_segments']:
        depDateTime = str(detail['dept_date_time'])
        depDateTime = depDateTime.split('T')
        depDateTime = " ".join(depDateTime)
        depDateTime = datetime.strptime(depDateTime, '%Y-%m-%d %H:%M:%S')
        arrDateTime = str(detail['arr_date_time'])
        arrDateTime = arrDateTime.split('T')
        arrDateTime = " ".join(arrDateTime)
        arrDateTime = datetime.strptime(arrDateTime, '%Y-%m-%d %H:%M:%S')

        prod_detailsList.append(
            CartProductDetails(cart_product_id=cartProduct.id, from_station=str(detail['dept_station']),
                               to_station=str(detail['arr_station']), from_code=str(detail['dept_station_code']),
                               to_code=str(detail['arr_station_code']),
                               departure_date=depDateTime, arrival_date=arrDateTime, train=str(detail['train']),
                               train_category=str(fare_class),
                               netprice=Money(fare, 'USD'), passengers_num=int(passengers_num)))

    CartProductDetails.objects.bulk_create(prod_detailsList)

    # print "cart product details created"

    # cart product passegers creation
    aldetails = []
    for passsenger in passengers:
        for i in passsenger:
            aldetails.append(CartProductPassengers(cart_product_id=cartProduct.id, first_name=i['first_name'],
                                                   last_name=i['secondname'], dob=datetime.now(),
                                                   nationality=i['nationality'], passport=i['passport'],
                                                   age=int(str(i['age']))))

    CartProductPassengers.objects.bulk_create(aldetails)
    # print "cart product passsengers  created"

    carts = Cart.objects.filter(sessionId=session_id)

    productAllDetails = CartProductDetails.objects.all()

    return [productAllDetails]


def summarydetail(request):
    ''' Summary Page '''
    if request.method == "POST":
        pass
    else:
        # print "summary page"
        productDetails = request.session.get('cart_products')

        for i in productDetails:
            # #print i
            for pro in i:
                # #print pro['netprice']
                price = pro['netprice'].encode('utf-8').strip()
                # print price
                # print type(price)
                # #print str(price).split('.')
        # #print len(productDetails), "555555555"
        return render(request, 'booking/summary.html', {'cartProducts': productDetails})


def summary1deta(request):
    ''' Summary Page one '''
    if request.method == "POST":
        pass
    else:
        # print "summary page"
        productDetails = request.session.get('cart_products')

        for i in productDetails:
            # #print i
            for pro in i:
                # #print pro['netprice']
                price = pro['netprice'].encode('utf-8').strip()
                # print price
                # print type(price)
                # #print str(price).split('.')
        # #print len(productDetails), "555555555"
        return render(request, 'booking/summary1.html', {'cartProducts': productDetails})
    # return render(request,'booking/summary1.html',{})
def pointdet(request):
    print ("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{")
    return render(request,)


def childAges(args):
    pass


# def allviewtest1(request):
#
#     srcpath=os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx")
#     cols = ['Location Code', 'Name','Country Code','Name', 'Is Synonym']
#     readpath_df=pd.read_excel(srcpath, usecols = cols)
#
#     # print (readpath_df.head(10),"[[[[[[[")
#     if request.method=="POST":
#         originStattion = request.POST.get('txtfromstation')
#         ####pandas type reading from excel
#         getdata = readpath_df.loc[readpath_df['Name'] == str(originStattion)]
#         #print(getdata,"}}}}}}}}}}}}}}}}")
#         from_loc_code = getdata['Location Code']
#         from_loc_code = getdata.iloc[0]['Location Code']
#         #print(from_loc_code, "rrrrrrrrr")
#         destStattion = request.POST.get('txttostation')
#         getdestdata = readpath_df[readpath_df['Name'] == str(destStattion)]
#         #print(type(getdestdata))
#         # print(getdestdata[1])
#         to_dest_code = getdestdata.iloc[0]['Location Code']
#         #print(to_dest_code, "PPPPPPPPPP")
#         departureDate = request.POST.get('txtfromdate')
#         departdatelist=str(departureDate)
#         #print (departdatelist,"))))))))))))))))))")
#         departdatelist1=datetime.strptime(str(departdatelist), '%d-%b-%Y').strftime('%Y-%m-%d')
#         #print(departdatelist1, "))))))))))))))))))")
#         departureTime = request.POST.get('Ddldeptime')
#         #print (departureTime,"---------------")
#         returnDate = request.POST.get('txttodate')
#         returnTime = request.POST.get('DdlReturntime')
#         numAdults = request.POST.get('DdlAdults')
#         numChilds = request.POST.get('DdlNonAdults')
#         childAges = json.loads(request.POST.get('childAges'))
#         #print(childAges,"cccccc")
#         # allages=[]
#         # if childAges>1:
#         #     for ch in childAges:
#         #         allages.append(ch)
#         # print allages
#         #print (originStattion,destStattion,departureDate,departureTime,returnDate)
#         #######xml format#########
#         root_text = '<?xml version="1.0" encoding="UTF-8"?>'
#         root = ET.Element('ACP_RailAvailRQ',ResponseType="Native-Availability", xmlns="http://www.acprailinternational.com/API/R2")
#         subroot=ET.SubElement(root,"POS")
#         sublevel2=ET.SubElement(subroot,"RequestorID").text = "RTG-XML"
#         sublevel3=ET.SubElement(root,'RailAvailInfo')
#         sublevel4=ET.SubElement(sublevel3,"OriginDestinationSpecifications")
#         sublevel5=ET.SubElement(sublevel4,"OriginLocation", LocationCode=str(from_loc_code))
#         sublevel6=ET.SubElement(sublevel4,"DestinationLocation", LocationCode=str(to_dest_code))
#         sublevel7 = ET.SubElement(sublevel4, "Departure", DepartureDate=departdatelist1+"T"+departureTime+":00")
#         #sublevel7 = ET.SubElement(sublevel4, "Departure",DepartureDate="2020-06-20T08:00:00")
#         sublevel8=ET.SubElement(sublevel3,"PassengerSpecifications")
#         sublevel19 = ET.SubElement(sublevel8, "PassengerType", Quantity="1", Age="-1")
#         for ch in childAges:
#             sublevel111=ET.SubElement(sublevel8,"PassengerType",Quantity="1",Age=ch)
#         sublevel20=ET.SubElement(sublevel3,"FareQualifier",RateCategory="Regular")
#         sublevel21=ET.SubElement(sublevel3,"ResponsePtPTypes")
#         sublevel22=ET.SubElement(sublevel21,"ResponsePtPType").text="TW"
#         #print (subrootlevel)
#
#         xml_data = ET.tostring(root)
#         # print(xml_data)
#         final_data = str(root_text) + str(xml_data)
#         #print(final_data,"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
#         headers = {'content-type': 'application/xml; charset=utf-8'}
#         callapidata = requests.post(url="https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ", data=final_data,headers=headers)
#         #print (callapidata,"cccccccccc")
#         if callapidata.status_code==200:
#             f=open("G:/testdata2.txt","w")
#             # callapidata=callapidata.decode("utf-8")
#             f1=f.write(callapidata.text)
#             f.close()
#             # print(callapidata.text)
#             #df = pd.DataFrame(callapidata.text)
#             #df.to_csv(r'F:/Sunitha_work_dq/shaik_submitted_proj/onlinebooking/pandas.txt', header=None, index=None, sep=' ', mode='a')
#             #print (callapidata.text,callapidata.status_code,"aaaa")
#             request.session['redirectdata12']=callapidata.text
#             #print(type(callapidata.text))
#             return redirect("/alltest/ticket1")
#             # return HttpResponseRedirect('/alltest/traveller_info')
#         else:
#             print("wrong status code")
#             return "Error"
#
#     else:
#         return render(request,'booking/index1.html',{})
def ticket_view1(request):
    if request.method=="POST":
        print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        return None
    else:
        #print ('wrong path')
        # callapidata=request.session.get('redirectdata12')
        # print(callapidata,"saaaaaaaaaaaaa")
        print("<<<<<<<<<<<<<<<$$$$$$$$$$$$$$$$$")
        f = open("G:/testdata.txt", "r")
        f1=f.read()
        print ("*****************")
        #print (type(f1))
        # print (f1,"HHHHHHHHHHHH")
        #f.close()
        #print(">>>>>>>>>>>>>>>>>>")
        my_dict = xmltodict.parse(f1)

        originlocat1=my_dict["ACP_RailAvailRS"]['OriginDestinationOptions']
        # print(originlocat1, ")))))))))55675656)))))))))")
        origin_station = my_dict["ACP_RailAvailRS"]['OriginDestinationOptions']['OriginDestinationOption'][str('OriginLocation')]
        print(origin_station,origin_station['@Name'],"))))))))))))))))))")
        journeys = my_dict["ACP_RailAvailRS"]['OriginDestinationOptions']['OriginDestinationOption']['Journeys']
        print(type(journeys), len(journeys))
        originlocat = my_dict["ACP_RailAvailRS"]['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']
        # print(originlocat, ")))))))))))\n")
        #print(type(originlocat))

        for data in originlocat:
            journey_segments = data['JourneySegments']
            journey_segment = journey_segments[str('JourneySegment')]
            train_segment = journey_segment['TrainSegment']
            departuredate=train_segment[str('@DepartureDateTime')]
            arrivaldate= train_segment[str('@ArrivalDateTime')]
            TrainNumber= train_segment[str('@TrainNumber')]
            JourneyDuration= train_segment[str('@JourneyDuration')]
            print(JourneyDuration)
        return render(request,'booking/tickets1.html',{})