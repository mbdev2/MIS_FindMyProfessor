# FindMyProfessor
## _Turn scriblles into words!_
![IMG_7240](https://user-images.githubusercontent.com/72226231/120156122-f1075200-c1f1-11eb-8e7c-4b92b1e53911.jpeg)


Tired of reading tiny scribbles on Zoom lectures? No worries, our solution enables PTZ cameras to auto-follow your professors' location.

Developed by Matjaž Bevc, Mark Breznik, Blaž Pridgar, and Eva Vidmar for a course in our undergraduate study program Multimedia at the Faculty of Electrical Engineering, University of Ljubljana

We would like to express a deep thank you to our mentor Luka Mali, who helped us whether any problems and encouraged us to set our goals high!

For a more detailed story, don't hesitate to check out Hackster: https://www.hackster.io/400488/mis-findmyprofessor-f5c445

## Features

- Track household purchases with a flick of your finger
- Figure out who owes who what
- Share a cloud-synced shopping list with your housemates
- Intuitively pay back what you own
- Play around with various color choices!

<img width="1671" alt="WebUI for the FindMyProfessor interface" src="https://user-images.githubusercontent.com/72226231/120156113-eea4f800-c1f1-11eb-9300-ed6476161262.png">


## Tech

FindMyProfessor uses several open-source and production projects to work properly:

- Bleak: Crazy powerful and modern BLE engine for Python
- Flask: Enables us to serve HTML websites from Python!
- Flask SocketIO: Refresh data dynamically with sockets, no bullshit required
- EdgeImpulse: Simply the easiest and most powerful online ML model designer, hats off!
- Arduino Nano 33 BLE: A tiny, affordable, and connected IoT board with TensorFlow capabilities.

And of course, FindMyProfessor itself is open source!

## Installation

For installation onto Arduino Nano 33 BLE, we recommend following the latest tutorial from EdgeImpulse Arduino Deployment, meanwhile for the Python Server side, just simply run the Python code and access your localhost address on port 5000.

## Development

For now, the development of FindMyProfessor has been finished - it was meant as a project for a University course, but we fell in love with the idea and Mark decided to pursue a similar project for his Bachelors's thesis.

## License

MIT
**Free Software, Hell Yeah!**
