from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .fcm import Fcm
from .models import Clients,Templates,Messages,Admin
from .serializers import ClientCouponsSerializer,TemplateSerializer,MessageSerializer,AdminSerializer
import base64
import csv
import StringIO

#Export to csv with filters
@api_view(['GET'])
def exportMessageToCSVWithFilter(request):
    start_time = request.GET['start_time']
    end_time = request.GET['end_time']



    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Messages.csv"'

    writer = csv.writer(response)
    writer.writerow(['Client Coupon', 'Company Name', 'Message Time', 'Message','Date','Time','Vendor','Name','Order Id','Sender','Amount'])

    messages = Messages.objects.all().order_by('-id')
    serializer = MessageSerializer(messages, many=True)
    for message in Messages.objects.raw(
            'SELECT * FROM kartylysis.SMS_messages where UNIX_TIMESTAMP(STR_TO_DATE(message_time,"%d/%m/%Y  %H:%i")) > 0 AND UNIX_TIMESTAMP(STR_TO_DATE(message_time,"%d/%m/%Y  %H:%i")) < 100000000000 Order by id desc'):
        writer.writerow(
            [message['client_coupon'], message['company_name'], message['message_time'], message['message'],
             message['date'], message['time'], message['vendor'], message['name'], message['orderId'],
             message['sender'], message['amount']])
    return response


#Export to csv
@api_view(['GET'])
def exportMessageToCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Messages.csv"'

    writer = csv.writer(response)
    writer.writerow(['Client Coupon', 'Company Name', 'Message Time', 'Message','Date','Time','Vendor','Name','Order Id','Sender','Amount'])

    messages = Messages.objects.all().order_by('-id')
    serializer = MessageSerializer(messages, many=True)
    for message in serializer.data:
        writer.writerow(
            [message['client_coupon'], message['company_name'], message['message_time'], message['message'], message['date'],  message['time'], message['vendor'], message['name'], message['orderId'],
             message['sender'],message['amount']])

    return response
#Update Client
@api_view(['POST'])
def updateClient(request):
    if request.method == 'POST':
        data = request.data
        id = data['client_id'];
        client = Clients.objects.filter(client_id=id).first()
        client.client_coupon = data['client_coupon'];
        client.phone_number = data['phone_number'];
        try:
            client.save();
        except:
            data['status'] = 0;
            return JsonResponse(data, safe=False)

        data['status'] = 1;
        return JsonResponse(data, safe=False)


#Upload CSV

@api_view(['POST'])
def uploadClientCSVData(request):
    if request.method == 'POST':
        data = request.data
        base64_string = data['base64EncodedCSV']
        csv_string = base64.b64decode(base64_string)
        f = StringIO.StringIO(csv_string)
        reader = csv.reader(f, delimiter=',')
        index = 0
        rowInserted = 0
        for row in reader:
            if index > 0:
                row[0] = row[0].decode('unicode_escape').encode('ascii','ignore').rstrip()
                row[1] = row[1].decode('unicode_escape').encode('ascii','ignore').rstrip()

                client = Clients(client_coupon=row[0],phone_number=row[1])
                try:
                    client.save()
                    rowInserted = rowInserted + 1;
                except:
                    index = index + 1
            index = index + 1
        output = {"total_row_inserted" : rowInserted}
        output['status'] = 'saved'
        return JsonResponse(output, safe=False)

# Get Template Messages
@api_view(['POST'])
def getTemplateMessages(request):
    if request.method == 'POST':
        data = request.data
        id = data['template_id']
        messages = Messages.objects.filter(template_id=id).order_by('-id')
        serializer = MessageSerializer(messages, many=True)
        data['data'] = serializer.data
        data['status'] = 'fetched'
        return JsonResponse(data, safe=False)


# Get User Messages
@api_view(['POST'])
def getUserMessages(request):
    if request.method == 'POST':
        data = request.data
        id = data['user_id']
        messages = Messages.objects.filter(user_id=id).order_by('-id')
        serializer = MessageSerializer(messages, many=True)
        data['data'] = serializer.data
        data['status'] = 'fetched'
        return JsonResponse(data, safe=False)


#ADD NEW TEMPLATE
@api_view(['POST'])
def updateTemplate(request):
    if request.method == 'POST':
        data = request.data
        id = data['id'];
        template = Templates.objects.filter(id=id).first()
        template.company_name = data['company_name'];
        template.sender_title = data['sender_title'];
        template.template_body = data['template_body'];
        template.save();
        Fcm.send_fcm_message(Fcm(), '{"id":' + str(id) + ', "tag" : "u"}')
        data['status'] = 'updated';
        return JsonResponse(data, safe=False)

#Delete NEW TEMPLATE
@api_view(['POST'])
def deleteTemplate(request):
    if request.method == 'POST':
        data = request.data
        id = data['id'];
        Templates.objects.filter(id=id).delete()
        Fcm.send_fcm_message(Fcm(), '{"id":' + str(id) + ', "tag" : "d"}')
        data['status'] = 'updated';
        return JsonResponse(data, safe=False)

#ADD NEW TEMPLATE
@api_view(['POST'])
def addNewTemplate(request):
    if request.method == 'POST':
        data = request.data
        serializer = TemplateSerializer(data=data)
        if serializer.is_valid():
            template = serializer.save()
            template = Templates.objects.latest('id')
            Fcm.send_fcm_message(Fcm(), '{"id":' + str(template.id) + ', "tag" : "a"}')
            templateJson = {'id':template.id}
            templateJson['company_name'] = template.company_name
            templateJson['template_body'] = template.template_body
            templateJson['sender_title'] = template.sender_title
            return JsonResponse(templateJson, safe=False)
        else:
            return JsonResponse(0, safe=False)





#Validate Admin
@api_view(['POST'])
def validateAdmin(request):
    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data['password']
        tasks = Admin.objects.filter(username=username,password=password)
        serializer = AdminSerializer(tasks, many=True)
        response_data = {'isValidUser':0,'id':0}

        if len(serializer.data) > 0 :
            response_data['isValidUser'] = 1
            response_data['id'] = serializer.data[0]['id']

        return JsonResponse(response_data, safe=False)


#Validate client token
@api_view(['POST'])
def validateClient(request):
    if request.method == 'POST':

        data = request.data
        client_coupon = data['client_coupon']
        phone_number = data['phone_number']

        tasks = Clients.objects.filter(client_coupon=client_coupon,phone_number=phone_number)
        serializer = ClientCouponsSerializer(tasks, many=True)
        response_data = {'isValidUser':0,'client_id':0}

        if len(serializer.data) > 0 :
            response_data['isValidUser'] = 1
            response_data['client_id'] = serializer.data[0]['client_id']
        return JsonResponse(response_data, safe=False)



# Get Post Templates
class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Templates.objects.all().order_by('-id')
    serializer_class = TemplateSerializer


# Get Post Messages
class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all().order_by('-id')
    serializer_class = MessageSerializer

# Get Post Clients
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all().order_by('-client_id')
    serializer_class = ClientCouponsSerializer

    # Validate Get Post Clients


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
