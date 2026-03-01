Quest TCP Chat System is a lightweight client-server application that demonstrates real-time text communication over TCP.

The tech stack is based on Python 3, using the standard library `socket` module to manage TCP connections and simple concurrency mechanisms (such as threads or select) to support multiple clients at the same time. The applications are implemented as straightforward command-line programs with no external dependencies, so they are easy to run on common desktop operating systems.

The project is composed of a relay server and one or more clients. The server is responsible for managing TCP connections, receiving messages from connected clients, and forwarding or broadcasting those messages to the appropriate recipients. This includes basic connection management, message routing, and simple broadcast capabilities so that multiple users can participate in a shared conversation.

On the client side, the application connects to the relay server, sends user-typed messages, and continuously listens for incoming messages from other participants. Clients can establish and close connections, enabling a simple lifecycle of connect, chat, and disconnect.

This project is suitable as a learning or demonstration tool for TCP-based networking concepts, including socket programming, message forwarding, and multi-client communication patterns.