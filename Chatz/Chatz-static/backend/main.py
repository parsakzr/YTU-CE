from flask.typing import StatusCode
from psycopg2 import connect
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from werkzeug.wrappers import response
import apiconnections
import auth
import channel
import connections
import guild
import message
app = Flask(__name__)
CORS(app)

"""
/user/create, POST method

You should be sending a POST with a JSON object like this:
{
    "username": "noonlord23",
    "password": "testpass"
}

Returns JSON: 
{
    "token": "3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f"
}
"""


@cross_origin(origin='*')
@app.route("/user/create", methods=["POST"])
def createUser():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = auth.createUser(username, password)
    return jsonify({"token": token})


"""
/user/login, GET method
Example usage:
http://localhost:23451/user/login?username=noonlord23&password=testpass

Returns JSON: 
{
    "token": "3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f"
}

"""


@app.route("/user/login")
def login():
    data = request.args
    username = data.get("username")
    password = data.get("password")
    token = auth.login(username, password)
    return jsonify({"token": token})


"""
/user/getUsername, GET method
Example usage:
http://localhost:23451/user/getUsername?id=13

Returns username: 

"noonlord2"

"""


@app.route("/user/getUsername")
def getUsername():
    data = request.args
    id = data.get("id")
    return jsonify(auth.getUsername(id))


"""
/guild/create, POST method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

You should be sending a POST with a JSON object like this:
{
    "guildName": "My Guild",
}

Returns ID of created guild
"""


@cross_origin(origin='*')
@app.route("/guild/create", methods=["POST"])
def createGuild():
    data = request.json
    guildName = data.get("guildName")
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    guildId = guild.createGuild(guildName, id)
    return jsonify(guildId)


"""
/guild/data, GET method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

Example usage:
http://localhost:23451/guild/data?guildId=4

Returns JSON: 
{
    "creatorId": 14,
    "guildName": "My Newest Guild"
}

"""


@app.route("/guild/data")
def guildData():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.args
    guildId = data.get("guildId")
    guildData = guild.getGuildData(guildId)
    return jsonify(guildData)


"""
/channel/create, POST method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

You should be sending a POST with a JSON object like this:
{
    "channelName": "My Channel",
    "guildId": 4
}
Returns ID of created channel
"""


@cross_origin(origin='*')
@app.route("/channel/create", methods=["POST"])
def createChannel():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.json
    channelName = data.get("channelName")
    guildId = data.get("guildId")
    channelId = channel.createChannel(channelName, guildId)
    return jsonify(channelId)


"""
/channel/guildChannels, GET method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

Example usage:
http://localhost:23451/channel/guildChannels?guildId=4

Returns JSON: 
[
    {
        "channelId": 5,
        "channelName": "My Channel"
    },
    {
        "channelId": 6,
        "channelName": "My Channel 2"
    },
    {
        "channelId": 7,
        "channelName": "My Channel 3"
    }
]

"""


@app.route("/channel/guildChannels")
def guildChannels():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.args
    guildId = data.get("guildId")
    guildData = channel.getGuildChannels(guildId)
    return jsonify(guildData)


"""
/connections/joinGuild, POST method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

You should be sending a POST with a JSON object like this:
{
    "guildId": 16
}
Returns OK
"""


@cross_origin(origin='*')
@app.route("/connections/joinGuild", methods=["POST"])
def joinGuild():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    data = request.json
    guildId = data.get("guildId")
    if connections.joinGuild(guildId, id):
        return Response(status=200)
    else:
        return Response(status=404)


"""
/connections/getGuilds, GET method

! No need for parameters, it will return based on the Token.

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

Returns JSON containing guild ID's: 
[
    16,
    5
]
"""


@app.route("/connections/getGuilds")
def getGuilds():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    data = connections.getGuildsOfUser(id)
    return jsonify(data)


"""
/connections/getGuildMembers, GET method

Example usage:
http://localhost:23451/connections/getGuildMembers?guildId=123

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

Returns JSON containing Member ID's: 
[
    123,
    125,
    126,
    127
]
"""


@app.route("/connections/getGuildMembers")
def getGuildMembers():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.args
    guildId = data.get("guildId")
    data = connections.getGuildMembers(guildId)
    return jsonify(data)


"""
/message/send, POST method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

You should be sending a POST with a JSON object like this:
{
    "message": "My amazing message",
    "channelId": 4
}

Returns OK
"""


@cross_origin(origin='*')
@app.route("/message/send", methods=["POST"])
def sendMessage():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.json
    messageText = data.get("message")
    channelId = data.get("channelId")
    if message.sendMessage(id, messageText, channelId):
        return Response(status=200)
    else:
        return Response(status=500)


"""
/message/getMessages, GET method

For authentication, you should include token on HTTP header, example HTTP Header:
'Token': '3db1fd20b3d37a65d62170616cbec961382e530f7ca257d8a4d516900f2be32f'

Example usage without after parameter:
http://localhost:23451/message/getMessages?channelId=4

Example usage with after parameter (UNIX time):
http://localhost:23451/message/getMessages?channelId=4&after=1640576468

Returns JSON: 

[
    {
        "content": "My amazing message",
        "messageId": 6,
        "senderId": 14,
        "time": 1640576468
    },
    {
        "content": "My amazing message",
        "messageId": 7,
        "senderId": 14,
        "time": 1640576483
    }
]

"""


@app.route("/message/getMessages")
def getMessages():
    token = request.headers.get("Token")
    id = auth.getUserId(token)
    # Buraya yetki kontrolü gelecek
    data = request.args
    channelId = data.get("channelId")
    after = data.get("after")
    if after:
        responseData = message.getMessages(channelId, after=after)
    else:
        responseData = message.getMessages(channelId)

    return jsonify(responseData)

# http://127.0.0.1:23451/api/getCoin?coin=btc
@app.route("/api/getCoin")
def getCoin():
    data = request.args
    coin = data.get("coin")
    if coin:
        coin = coin.upper()
        value = apiconnections.get_coin(coin)
        if value != -1:
            return jsonify(value)
        else:
            return response(StatusCode = 404)

# http://127.0.0.1:23451/api/getCurrency?currency=usd
@app.route("/api/getCurrency")
def getCurrency():
    data = request.args
    currency = data.get("currency")
    if currency:
        currency = currency.upper()
        value = apiconnections.get_currency(currency)
        if value != -1:
            return jsonify(value)
        else:
            return Response(status = 404)
    return Response(status = 400)

# http://127.0.0.1:23451/api/getWeather?city=Edirne
@app.route("/api/getWeather")
def getWeather():
    data = request.args
    city = data.get("city")
    if city:
        temp = apiconnections.get_weather(city)
        if temp != -1:
            return jsonify(temp)
        else:
            return Response(status = 404)
    return Response(status=400)

@app.route("/user/getAll")
def getAll():
    return jsonify(connections.getAllMembers())

if __name__ == "__main__":
    app.run(debug=True, port=23451)
