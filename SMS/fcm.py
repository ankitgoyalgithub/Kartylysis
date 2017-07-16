import urllib2

class Fcm():
    def send_fcm_message(self,data):
        data = '{"to":"/topics/Kartylysis","data":' + data +'}'
        url = 'https://fcm.googleapis.com/fcm/send'
        req = urllib2.Request(url, data, {'Content-Type': 'application/json',
                                          'Authorization': 'key=AAAA-C9h-bU:APA91bEuLpQzulhtRExDC6XDcCi_abaLIAL_w6U22T74VKNXE1G-S5FX_uLJGKaL856BG09QylpuFTrbXmbSagedxstjfzcw27wqGrLloa9HXaQJNYxwrd6e_5RwudsdOV9CjQ4SlFk9'})
        f = urllib2.urlopen(req)