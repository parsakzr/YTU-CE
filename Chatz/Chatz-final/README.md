# Chatz - Messajlaşma Sistemi
*Build Instructions*

<br/>

## `Backend`

* ### python
python3 ile yazılan backend, ```backend/``` klasöründe mevcuttur.
dependency olarak, flask ve psycop2 package'lerine ihtiyaci vardır.
> `pip3 install flast` ve `pip3 install psycopg2`

ve sunucu hizmetini başlatmak için
> `python main.py`


* ### Veritabanı
Veritabani PostgreSQL olarak ```chatzdbBackup``` dosyasindan restore edilebilir. 
( chatz adlı kullanıcı Owner olması önemli )
> dbname=chatzdb user=chatz password=chatz 

olarak şekilde bir database oluşturulur ve restore edilir.


## `Web Client`

Node.js ve npm yüklü olma şartıyla, `chatz` ana klasörde bu komut ile `package.json` da olan dependencyleri alinabilir:
> `npm install`

ve client hizmetini [http://localhost:3000](http://localhost:3000)'de başlatmak için
> `npm run start`

ve client'i `/build` klasorde build build yapmak için:
> `npm run build`


<hr/>

* [Rapor](https://docs.google.com/document/d/1cpmiOba_RQZ68LtNWQlbvwZxrWCYGvim-MvDSMzD5Y0/edit?usp=sharing)
* [Github](https://github.com/parsakzr/Chatz)
