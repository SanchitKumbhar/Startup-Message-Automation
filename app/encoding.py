import base64
import rsa
import pandas
with open("pub.pem","rb") as f:
    public_key=rsa.PublicKey.load_pkcs1(f.read())

with open("pri.pem","rb") as f:
    private_key=rsa.PrivateKey.load_pkcs1(f.read())



def encryption(dataframe):
    # for i in range(len(dataframe['Name'].values.tolist()[0])):
    #     for 
    newdf = {
        'Name': [],
        'Phone': [],
        'Amount': [],
        'Date': [],
        'PaymentPeriod': [],
        'firstMsg': [],
        'secondMsg': [],
        # 'companyName' : []
    }

    data=dataframe.values.tolist()
    new_dim_data = [item for i in data for item in i]
    key_list=[]
    for key in newdf:
         key_list.append(key)


    for i in range(len(new_dim_data)):
            for j in range(len(new_dim_data[0])):
                enc=rsa.encrypt(str(new_dim_data[i][j]).encode(),public_key)
                encrypted_data = base64.b64encode(enc).decode('utf-8')

                newdf[key_list[i]].append(encrypted_data)

    return pandas.DataFrame(newdf)

    
    