import paho.mqtt.client as mqtt
import rtmidi.midiutil as midi
import midi2mqtt.config as config
import argparse


class Midi2Broker:
    """Receiving MIDI events and sending them to an MQTT broker."""

    def __init__(self, host, port, midi_port):
        self.midiin, port_name = midi.open_midiinput(midi_port)
        print("listening to midi device", port_name)
        self.midiin.set_callback(self.on_midi_event)

        print("connecting and sending msgs to", host, port)
        self.mqtt = mqtt.Client()
        self.mqtt.connect(host, port)

    def on_midi_event(self, event, data=None):
        message, _ = event
        chan, note, val = message

        self.publish("midi/chan/{0}/note/{1}/".format(chan, note), val)

    def publish(self, topic, payload):
        self.mqtt.publish(topic, payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="Host of the MQTT-Broker",
                        default="localhost")
    parser.add_argument('port', help="Port of the MQTT-Broker",
                        type=int, default=1883)
    parser.add_argument('midiport', help="Port of the MIDI Interface",
                        type=int, default=1)
    args = parser.parse_args()

    client = Midi2Broker(args.host,
                         args.port,
                         args.midiport)

    print('Use a client to watch mqtt messages: mosquitto_sub -h {} -t "midi/#" -v'.
          format(args.host))

    print("finished")

if __name__ == "__main__":
    main()
