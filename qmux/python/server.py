import asyncio, pdb
from qmux import Session, TCPConn, IConn, DataView, empty_array

async def handle_echo(reader, writer):
    conn = TCPConn(reader, writer)
    sess = Session(conn, loop.create_task)
    
    channel = await sess.open()
    channel.write(b"tester echo")
    await channel.close_write()
    channel = await sess.accept()
    
    data = await channel.read(11) # qmux: unexpected packet in response to channel open: <nil>
    message = data.decode()
    print(message)
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    print("Client socket closed")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 9998, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
