# Anemoi
A full suite of software to collect and broadcast wind data through websockets and OSC using a Raspberry pi and an Anemometer

# Shopping list

[Add a list of links to all the material]

# Raspberry pi setup

[Add a schema of the wiring here]

# Running Anemoi on the pi

Anemoi can run in AP mode (that generates a local wifi network to connect to from the clients) or internet mode where the nodeJS server runs on the internet and the wind data is broadcast to all the connected clients.

## Configuration

Edit the config.json file and configure the ports, server name and mode. If AP_mode is true, the webserver option will be ignored and 'localhost' will be used instead.

## Internet mode (AP_mode = false)

After all configuration and wiring done all that needs to be done is to run anemoi:
```
python anemoi.py
```

If you have multiple config files you can specify which you want to use from the command line:

```
python anemoi.py config02.json
```
## Wireless AP mode (AP_mode = true)

[Explain configuration of AP mode here]

After you have your ap running, make sure you have AP_mode set to true on the cofig file and run anemoi.py as usual.
