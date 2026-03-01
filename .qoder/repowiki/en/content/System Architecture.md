# System Architecture

<cite>
**Referenced Files in This Document**
- [chat_client.py](file://chat_client.py)
- [chat_server.py](file://chat_server.py)
- [README.md](file://README.md)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)

## Introduction
The Wipan Qoder system implements a simple TCP socket-based chat application following a client-server architecture pattern. The system demonstrates real-time messaging capabilities through a relay server that broadcasts messages from one client to all other connected clients. This document provides comprehensive architectural analysis covering the observer pattern implementation, threading model, TCP socket communication flow, and thread-safety mechanisms.

## Project Structure
The project consists of two primary components: a client-side application and a server-side relay system.

```mermaid
graph TB
subgraph "Wipan Qoder System"
subgraph "Client Side"
CC[chat_client.py<br/>TCP Client Implementation]
end
subgraph "Server Side"
CS[chat_server.py<br/>TCP Server Implementation]
end
subgraph "Network Layer"
TC[TCP Sockets<br/>127.0.0.1:9999]
end
CC --> TC
TC --> CS
end
```

**Diagram sources**
- [chat_client.py](file://chat_client.py#L1-L54)
- [chat_server.py](file://chat_server.py#L1-L75)

**Section sources**
- [chat_client.py](file://chat_client.py#L1-L54)
- [chat_server.py](file://chat_server.py#L1-L75)
- [README.md](file://README.md#L1-L2)

## Core Components
The system comprises two fundamental components that work together to provide real-time messaging functionality:

### Client Component
The client implementation handles network communication, user input processing, and message display. It establishes TCP connections to the server, manages bidirectional communication, and provides a simple console interface for user interaction.

### Server Component  
The server implementation manages multiple client connections, maintains connection state, and implements the message broadcasting mechanism. It handles client registration, message relaying, and connection lifecycle management.

**Section sources**
- [chat_client.py](file://chat_client.py#L22-L54)
- [chat_server.py](file://chat_server.py#L48-L75)

## Architecture Overview
The Wipan Qoder system follows a classic client-server architecture with a central relay server managing all client communications.

```mermaid
graph TB
subgraph "Client Applications"
C1[Client 1<br/>User Interface]
C2[Client 2<br/>User Interface]
C3[Client N<br/>User Interface]
end
subgraph "Relay Server"
SS[Socket Server<br/>Thread Pool]
BC[Broadcast Engine<br/>Observer Pattern]
CM[Connection Manager<br/>Thread-Safe Registry]
end
subgraph "Network Infrastructure"
NET[TCP/IP Network<br/>127.0.0.1:9999]
end
C1 --> NET
C2 --> NET
C3 --> NET
NET --> SS
SS --> BC
SS --> CM
BC --> NET
NET --> C1
NET --> C2
NET --> C3
style SS fill:#e1f5fe
style BC fill:#f3e5f5
style CM fill:#e8f5e8
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L8-L20)
- [chat_server.py](file://chat_server.py#L22-L46)
- [chat_client.py](file://chat_client.py#L9-L20)

## Detailed Component Analysis

### Client-Server Communication Flow

The communication flow between clients and server follows a well-defined sequence that ensures reliable message delivery and real-time interaction.

```mermaid
sequenceDiagram
participant Client as Client Application
participant Server as Chat Server
participant Broadcast as Broadcast Engine
participant Registry as Connection Registry
Client->>Server : TCP Connect (127.0.0.1 : 9999)
Server->>Client : Request Name (Enter your name : )
Client->>Server : Send Username
Server->>Registry : Add Connection (thread-safe)
Server->>Broadcast : Notify Join Event
Broadcast->>Client : Welcome Message
loop Real-Time Messaging
Client->>Server : Send Message
Server->>Broadcast : Relay Message
Broadcast->>Client : Forward Message (excluding sender)
Broadcast->>Client : Forward Message (excluding sender)
Broadcast->>Client : Forward Message (excluding sender)
end
Client->>Server : Disconnect
Server->>Registry : Remove Connection (thread-safe)
Server->>Broadcast : Notify Leave Event
Broadcast->>Client : Goodbye Message
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L56-L66)
- [chat_server.py](file://chat_server.py#L22-L46)
- [chat_client.py](file://chat_client.py#L26-L35)

### Observer Pattern Implementation for Message Broadcasting

The server implements the observer pattern to manage message distribution to all connected clients. The broadcast mechanism acts as the subject, while each connected client serves as an observer.

```mermaid
classDiagram
class ChatServer {
-clients : List[socket.socket]
-lock : threading.Lock
+broadcast(message : bytes, sender : socket.socket) void
+handle_client(conn : socket.socket, addr : tuple, name : str) void
+main() void
}
class BroadcastEngine {
-lock : threading.Lock
-clients : List[socket.socket]
+notifyObservers(message : bytes, sender : socket.socket) void
+addObserver(client : socket.socket) void
+removeObserver(client : socket.socket) void
}
class ClientConnection {
+socket : socket.socket
+address : tuple
+username : str
+send(message : bytes) void
+receive() bytes
+close() void
}
class MessageRelay {
+relayMessage(sender : socket.socket, message : str) void
+formatMessage(username : str, text : str) str
}
ChatServer --> BroadcastEngine : "uses"
ChatServer --> ClientConnection : "manages"
BroadcastEngine --> ClientConnection : "observes"
MessageRelay --> BroadcastEngine : "formats"
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L8-L20)
- [chat_server.py](file://chat_server.py#L22-L46)

### Threading Model and Concurrency Management

The system employs a multi-threaded architecture to handle concurrent client connections efficiently. Each client connection spawns a dedicated thread for processing, enabling true parallelism in message handling.

```mermaid
graph TB
subgraph "Server Thread Pool"
ST[Server Thread<br/>Accept Connections]
HT[Handler Threads<br/>Per-Client Processing]
BT[Broadcast Thread<br/>Message Distribution]
end
subgraph "Client Threads"
CT1[Client Thread 1<br/>Receive Messages]
CT2[Client Thread 2<br/>Receive Messages]
CTN[Client Thread N<br/>Receive Messages]
end
subgraph "Shared Resources"
LR[Lock Resource<br/>threading.Lock]
CR[Connection Registry<br/>List[socket]]
end
ST --> HT
HT --> CT1
HT --> CT2
HT --> CTN
HT --> BT
BT --> LR
BT --> CR
style ST fill:#ffecb3
style HT fill:#e1f5fe
style BT fill:#f3e5f5
style LR fill:#ffebee
style CR fill:#e8f5e8
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L63-L66)
- [chat_server.py](file://chat_server.py#L12-L20)

### TCP Socket Communication Protocol

The system implements a straightforward TCP-based communication protocol with clear message boundaries and connection lifecycle management.

```mermaid
flowchart TD
Start([Connection Established]) --> NameReq["Server sends name request"]
NameReq --> NameRecv["Client receives name prompt"]
NameRecv --> NameSend["Client sends username"]
NameSend --> NameAck["Server acknowledges name"]
NameAck --> Ready["Server marks client ready"]
Ready --> MsgLoop{"Message Available?"}
MsgLoop --> |Yes| ReceiveMsg["Receive message from client"]
MsgLoop --> |No| MsgLoop
ReceiveMsg --> ValidateMsg["Validate message content"]
ValidateMsg --> FormatMsg["Format message with username"]
FormatMsg --> BroadcastMsg["Broadcast to all clients"]
BroadcastMsg --> SendToClients["Send formatted message to each client"]
SendToClients --> Acknowledge["Client acknowledges receipt"]
Acknowledge --> MsgLoop
ReceiveMsg --> |Client disconnects| Cleanup["Remove client from registry"]
Cleanup --> BroadcastLeave["Broadcast leave message"]
BroadcastLeave --> CloseConn["Close client connection"]
CloseConn --> End([Connection Closed])
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L56-L66)
- [chat_server.py](file://chat_server.py#L22-L46)
- [chat_client.py](file://chat_client.py#L29-L35)

**Section sources**
- [chat_client.py](file://chat_client.py#L9-L20)
- [chat_server.py](file://chat_server.py#L12-L20)
- [chat_server.py](file://chat_server.py#L22-L46)

## Dependency Analysis

The system exhibits minimal coupling between components, with clear separation of concerns between client and server responsibilities.

```mermaid
graph TB
subgraph "External Dependencies"
TS[Threading Module]
SO[Socket Module]
SY[Sys Module]
end
subgraph "Internal Dependencies"
CC[chat_client.py]
CS[chat_server.py]
BC[broadcast function]
HC[handle_client function]
MC[main function]
end
TS --> CC
TS --> CS
SO --> CC
SO --> CS
SY --> CC
SY --> CS
CC --> MC
CS --> BC
CS --> HC
CS --> MC
style CC fill:#e3f2fd
style CS fill:#f3e5f5
style BC fill:#e8f5e8
style HC fill:#fff3e0
style MC fill:#fce4ec
```

**Diagram sources**
- [chat_client.py](file://chat_client.py#L1-L4)
- [chat_server.py](file://chat_server.py#L1-L4)

### Thread-Safety Mechanisms and Lock-Based Synchronization

The server implements robust thread-safety mechanisms to protect shared resources during concurrent access scenarios.

```mermaid
sequenceDiagram
participant T1 as Thread 1
participant T2 as Thread 2
participant Lock as threading.Lock
participant Clients as Shared Registry
T1->>Lock : acquire()
Lock-->>T1 : lock acquired
T1->>Clients : modify registry
T1->>Lock : release()
Lock-->>T1 : lock released
T2->>Lock : acquire()
Lock-->>T2 : blocked until T1 releases
T2->>Lock : acquire() succeeds
T2->>Clients : modify registry
T2->>Lock : release()
Lock-->>T2 : lock released
```

**Diagram sources**
- [chat_server.py](file://chat_server.py#L8-L9)
- [chat_server.py](file://chat_server.py#L12-L20)

**Section sources**
- [chat_server.py](file://chat_server.py#L8-L9)
- [chat_server.py](file://chat_server.py#L12-L20)

## Performance Considerations

The system demonstrates several performance characteristics that impact scalability and resource utilization:

### Scalability Factors
- **Connection Limit**: Each client spawns a dedicated thread, limiting concurrent connections based on system resources
- **Memory Usage**: Maintains a list of active client connections in memory
- **Network Throughput**: Single-threaded broadcast operation may become a bottleneck with many clients
- **CPU Utilization**: Each active client consumes CPU cycles for message processing

### Optimization Opportunities
- Implement connection pooling for better resource management
- Consider asynchronous I/O for improved throughput
- Add connection limits and rate limiting
- Implement message queuing for high-volume scenarios

## Troubleshooting Guide

### Common Connection Issues
- **Connection Refused**: Verify server is running and listening on correct IP/port
- **Name Registration Failures**: Ensure client sends non-empty username during handshake
- **Message Delivery Failures**: Check network connectivity and firewall settings

### Thread Safety Issues
- **Race Conditions**: Monitor for concurrent modifications to client registry
- **Deadlocks**: Ensure proper lock acquisition order in all code paths
- **Resource Leaks**: Verify proper cleanup of closed connections

### Debugging Strategies
- Enable verbose logging for connection events
- Monitor thread count and resource usage
- Test with multiple concurrent clients
- Validate graceful shutdown procedures

**Section sources**
- [chat_server.py](file://chat_server.py#L36-L45)
- [chat_client.py](file://chat_client.py#L18-L20)

## Conclusion

The Wipan Qoder system successfully implements a client-server architecture for real-time messaging with clear separation of concerns and robust thread-safety mechanisms. The system demonstrates effective use of the observer pattern for message broadcasting and provides a solid foundation for understanding distributed communication patterns.

Key architectural strengths include:
- Clear client-server separation with well-defined protocols
- Effective observer pattern implementation for scalable message distribution
- Robust thread-safety mechanisms protecting shared resources
- Simple, maintainable code structure suitable for educational purposes

The system serves as an excellent example of fundamental networking concepts and can be extended with additional features such as message persistence, user authentication, and advanced concurrency patterns.