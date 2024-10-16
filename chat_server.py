import asyncio
import aio_pika

async def start_server():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("chat", durable=True)

    async def callback(message: aio_pika.IncomingMessage):
        async with message.process():
            print(f"Received: {message.body.decode()}")
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.body),
                routing_key="chat"
            )

    await queue.consume(callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    await asyncio.Future() 

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Server stopped by user")