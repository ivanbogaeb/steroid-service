from flask import jsonify
import types

def usage(Hardware):

    response = []

    for connection in Hardware:
        print(connection.Name)
        response.append(connection.Name)

    return jsonify(response)