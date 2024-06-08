import requests

url = "https://www.fast2sms.com/dev/bulkV2"
name = "sanchit"
phone = 8010235068
msg = {"This is a test message"}
payload = f"message={msg}&language=english&route=q&numbers={phone}"
headers = {
    'authorization': "h0FwasPTgkfSvupCxQo4rtXbe6qKlW58JVEUNMYmBRy2Oz7DH190LVnWHX5k41JbqNhBmMyRwPlOa3c2",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

# import requests

# url = "https://www.fast2sms.com/dev/bulkV2"

# payload = "message=This%20is%20a%20test%20message&language=english&route=q&numbers=9999999999,8888888888,7777777777"
# headers = {
#     'authorization': "h0FwasPTgkfSvupCxQo4rtXbe6qKlW58JVEUNMYmBRy2Oz7DH190LVnWHX5k41JbqNhBmMyRwPlOa3c2",
#     'Content-Type': "application/x-www-form-urlencoded",
#     'Cache-Control': "no-cache",
#     }

# response = requests.request("POST", url, data=payload, headers=headers)


# print(response.text)
