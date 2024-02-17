
import requests
from flask import Flask, request
import http

WAAPI_TOKEN = "YOUR_WAAPI_TOKEN"
WAAPI_INSTANCE = "YOUR_WAAPI_INSTANCE_ID"

#example of a menu with submenus
rutas = {
    "1": {
        "text": "ruta 1 activa envia 1 para activar subruta 1-1, 2 para activar subruta 1-2 envia 0 para volver a la ruta principal",
        "subrutas":{
            "1": {
                "text": "subruta 1-1 activa envia 1 para activar subsubruta 1-1-1, 2 para activar subsubruta 1-1-2 envia 0 para volver a la ruta principal",
                "subrutas": {
                    "1": {
                        "text": "subsubruta 1-1-1 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    },
                    "2": {
                        "text": "subsubruta 1-1-2 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    }
                }
            },
            "2": {
                "text": "subruta 1-2 activa envia 1 para activar subsubruta 1-2-1, 2 para activar subsubruta 1-2-2 envia 0 para volver a la ruta principal",
                "subrutas": {
                    "1": {
                        "text": "subsubruta 1-2-1 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    },
                    "2": {
                        "text": "subsubruta 1-2-2 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    }
                }
            }
        }
    },
    "2": {
        "text": "ruta 2 activa envia 1 para activar subruta 2-1, 2 para activar subruta 2-2 envia 0 para volver a la ruta principal",
        "subrutas":{
            "1": {
                "text": "subruta 2-1 activa envia 1 para activar subsubruta 2-1-1, 2 para activar subsubruta 2-1-2 envia 0 para volver a la ruta principal",
                "subrutas": {
                    "1": {
                        "text": "subsubruta 2-1-1 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    },
                    "2": {
                        "text": "subsubruta 2-1-2 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    }
                }
            },
            "2": {
                "text": "subruta 2-2 activa envia 1 para activar subsubruta 2-2-1, 2 para activar subsubruta 2-2-2 envia 0 para volver a la ruta principal",
                "subrutas": {
                    "1": {
                        "text": "subsubruta 2-2-1 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    },
                    "2": {
                        "text": "subsubruta 2-2-2 activa envia 0 para volver a la ruta principal",
                        "subrutas": {
                            "0":{
                                "text": "regresando a la ruta principal"
                            }
                        }
                    }
                }
            }
        }
    },
}

#active routes are stored here to keep track of the user's location in the menu
rutas_activas = {
}

app = Flask(__name__)

#webhook to receive messages from WAAPI
@app.route('/webhook/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        return "No data received", http.HTTPStatus.BAD_REQUEST
    
    #check if the message is a chat message and not a system message or a message from a group, voice, etc
    if (data["data"]["message"]["type"] == "chat") and  (not "subtype" in data["data"]["message"]):
        body = str(data["data"]["message"]["_data"]["body"])
        sender = str(data["data"]["message"]["_data"]["from"])
        if sender in rutas_activas:
            if body == "0":
                rutas_activas.pop(sender)
                send_whatsapp_WAAPI(sender[:-5], "volviendo a la ruta principal")
            elif body in rutas_activas[sender]["subrutas"]:
                rutas_activas[sender] = rutas_activas[sender]["subrutas"][body]
                send_whatsapp_WAAPI(sender[:-5], rutas_activas[sender]["text"])
            else:
                send_whatsapp_WAAPI(sender[:-5], "opcion invalida")
        else:
            if body in rutas:
                rutas_activas[sender] = rutas[body]
                send_whatsapp_WAAPI(sender[:-5], rutas[body]["text"])

    return "Data received", http.HTTPStatus.OK

#function to send a message to a user using WAAPI
def send_whatsapp_WAAPI(send_to: str, message: str):
    url = "https://waapi.app/api/v1/instances/"+WAAPI_INSTANCE+"/client/action/send-message"

    payload = {
        "message": message,
        "chatId": send_to+"@c.us"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer "+WAAPI_TOKEN
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
