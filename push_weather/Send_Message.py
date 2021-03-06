from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_message(info):
    json = "{" \
        "\"girlfriend\":\"" + info['gf'] + "\"," \
        "\"mynickname\":\"" + info['nickname'] + \
        "\",\"day\":\"" + info['day'] + "\","\
        "\"weather\":\"" + info['weather'] + "\","\
        "\"temp\":\"" + info['temp'] + "\","\
        "\"tips\":\"" + info['tips'] + "\""\
        "}"
    client = AcsClient(info['AI'], info['AK'], 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', info['phone'])
    # request.add_query_param('PhoneNumbers', "17300989938")
    request.add_query_param('SignName', "BaldFish")
    request.add_query_param('TemplateCode', "SMS_212690178")
    request.add_query_param('TemplateParam', json)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
