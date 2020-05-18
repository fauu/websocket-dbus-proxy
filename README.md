# websocket-dbus-proxy

Creates a websocket server that forwards messages received through dbus. Requires Python 3.


## Example use-cases

The script was created to make possible controlling the [LiveSplit One](https://github.com/LiveSplit/LiveSplitOne) speedrunning timer, which is a web application, using global keyboard shortcuts.

## Usage example

The following usage example is based on the particular use-case described above.

First, clone the repository or download and unpack the source. Enter the directory.

Install dependencies, for example:

````bash
pip install -r requirements.txt
````

Create a global keyboard shortcut that will send a dbus message to the script, containing a command recognizable by LiveSplit One. The following example binds the `space` key to the LiveSplit One command `splitorstart` in the i3 window manager configuration file:

````
bindsym space exec dbus-send --session --type=signal / com.github.fauu.websocket_dbus_proxy string:'splitorstart'
````

Run the script, specifying a port for the websocket server, for example:

````bash
python websocket-dbus-proxy.py 1111
````

The script should report the address of the websocket server, for example:

````bash
Websocket dbus proxy running at ws://localhost:1111…
````

Open https://one.livesplit.org/.

Click "Connect to Server" button.

Enter the fully qualified websocket server address, in our example `ws://localhost:1111`.

You should now be able to start the timer or split it if it's already running using the `space` button, even with the browser window running LiveSplit One out of focus.
