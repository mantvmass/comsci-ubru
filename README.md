COMSCI-UBRU
=========== 
A site for organizing freshman activaties for shools or universities.

**Start server**  

    > # Clone the source  or Download source
    > git clone https://github.com/mantvmass/comsci-ubru  

    > # Open cmd and change path
    > cd path/to/comsci
    
    > # Install package
    > pip install -r requrements.txt
    
    > # Run
    > python server.py

### setting
config database and path
```python
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306 # MariaDB dafault port 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'comsci'

# Edit generate qr function
def generate_qr(token):
    try:
        name = timestamp() # get for timestamp function
        data = "https://comsci-ubru.tk/view?token={}".format(token) # change to your url path
        qr = qrcode.QRCode(version=1, box_size=8, border=3)
        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(fill='black', back_color='white')
        image.save('static/image/qrcode/{}.png'.format(name))
        return str(name)
    except Exception:
        return False

```
                                                                                                                                       
Supports
----------------------
* Windows server
* Linux ( Ubuntu )

API
---
In process.

License
---------
- [MIT](https://github.com/mantvmass/comsci-ubru/blob/main/LICENSE)
