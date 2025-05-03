import mongoengine

mongoengine.connect(
    db='attack_data',
    host='localhost',
    port=27017  
)