# Peer
Sublime plugin to create remote peer programming sessions. Connects to
[Peer Server](https://github.com/jltorresm/peer-server) that manages the sessions.

### Important! Read Before Continuing
This is a basic proof of concept for a functional peer programming plugin. The current implementation has several
limitations and tons of optimizations can be made.

Some of the limitations:

- Communication is unidirectional. That is, the user who creates the session can write content, the rest can only watch.
- You MUST self-host the [Peer Server](https://github.com/jltorresm/peer-server). I am not providing a public server to
  manage the sessions.
- There is no authentication implemented so be careful how you use this.
- The communication is done via HTTP, I left the S out on purpose (be careful with what you transmit).

## Installation
1. Install plugin using `Package Control`.
2. Configure your [Peer Server](https://github.com/jltorresm/peer-server) URL in `Preferences -> Package Settings -> Peer -> Settings`

## Usage
### Start a session
- Locate in the view that you want to share.
- `Right click -> Peers -> Create a Session`
- Copy your `session id`.
- Share it with the other participants.

### Join a session
- In any view, `Right click -> Peers -> Join a Session`
- Enter the `session id` in the box and press enter.
- A new view will open and the session will start.

### Stop session
- In any view, `Right click -> Peers -> Stop Current Session`
- Or simply, close the view that you are sharing or that you joined.

## Settings

#### peer_server_url
_type_   : **string**

_default_: **null**

_description_: URL of the Peer server to use for the coding session.
