# Project 7: Multi-Client TCP Chat Server
**Course:** Parallel and Distributed Computing
**CLO 5 Target:** Framework – TCP sockets, client-server with one thread per client.

## Command List

| Command | Syntax | Description |
| :--- | :--- | :--- |
| **/nick** | `/nick <name>` | Sets or changes the user's display name. Returns an error if the name is already taken by another active user. |
| **/msg** | `/msg <name> <text>` | Sends a private message to the specified user. Returns an error if the target user is offline. |
| **/quit** | `/quit` | Disconnects the client from the server, cleans up the socket, and broadcasts a "[User] has left" message. |
| *(none)* | `<text>` | Any standard text typed without a slash will be broadcast to all currently connected users. |