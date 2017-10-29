import paho.mqtt.client as mqtt
import configparser
import rtmidi.midiutil as midi
import midi2mqtt.config as config


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
    client = Midi2Broker(config.mqtt_host,
                         config.mqtt_port,
                         config.midi_port)

    print('Use a client to watch mqtt messages: mosquitto_sub -h {} -t "midi/#" -v'.
          format(config.mqtt_host))

    print("finished")

if __name__ == "__main__":
    main()
    
