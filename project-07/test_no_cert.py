# test_no_cert.py - Should be REJECTED
# Waits 3 seconds for the broker's response, because with TLS 1.3 the broker
# rejects a missing client certificate just after connect() returns.
import time
import ssl
import paho.mqtt.client as mqtt

try:
    MQTT_CLIENT_ARGS = {"callback_api_version": mqtt.CallbackAPIVersion.VERSION1}
except AttributeError:
    MQTT_CLIENT_ARGS = {}

result = {"connected": False, "reason": None}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        result["connected"] = True

def on_disconnect(client, userdata, rc):
    result["reason"] = f"broker closed the connection (rc={rc})"

client = mqtt.Client(client_id="rogue-device", **MQTT_CLIENT_ARGS)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Only CA cert, NO client certificate
client.tls_set(ca_certs="certs/ca.pem")

try:
    client.connect("localhost", 8883, keepalive=60)
    client.loop_start()
    time.sleep(3)
    client.loop_stop()
except Exception as e:
    result["reason"] = str(e)

if result["connected"]:
    print("ERROR: Connection was accepted - check your config!")
else:
    print(f"SUCCESS: Connection rejected: {result['reason'] or 'no MQTT session was established'}")