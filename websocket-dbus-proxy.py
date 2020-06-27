import asyncio
import socket
import sys

import dbussy as dbus
from dbussy import DBUS
import websockets


cmd_queue = asyncio.Queue()


async def producer_handler(websocket, path):
    while True:
        cmd = await cmd_queue.get()
        cmd_queue.task_done()
        print("Forwarded command: '{}'".format(cmd))
        await websocket.send(cmd)


async def message_filter(connection, message, data):
    if (
        message.interface == "com.github.fauu"
        and message.member == "websocket_dbus_proxy"
    ):
        cmd = list(message.objects)[0]
        print("Received command: '{}'".format(cmd))
        cmd_queue.put_nowait(cmd)
    return DBUS.HANDLER_RESULT_HANDLED


def main(argv):
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <port>", file=sys.stderr)
        return 1
    port = argv[1]

    start_server = websockets.serve(producer_handler, "localhost", port)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server)
    except socket.gaierror:
        print(f"Specified port '{port}' is incorrect", file=sys.stderr)
        return 1
    except OSError as err:
        if err.errno == 98:
            print(
                f"Specified port '{port}' is already in use (is another instance already running?)",
                file=sys.stderr,
            )
        else:
            print(f"Unknown operating system error", file=sys.stderr)
        return 1

    print(f"Websocket dbus proxy running at ws://localhost:{port}…")

    conn = dbus.Connection.bus_get(DBUS.BUS_SESSION, private=False)
    conn.attach_asyncio(loop)
    conn.add_filter(message_filter, None)
    conn.bus_add_match("type=signal")

    print("Waiting for commands…")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nExiting…")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
