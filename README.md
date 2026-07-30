# Proxy Manager GUI

This project provides a graphical user interface (GUI) for the **V2Ray/Xray Core**, allowing you to add and use proxy URLs more easily.

## Important Requirements

Before using this application, you must have **Xray Core installed** on your system.

The Xray executable must also be added to your system's **PATH** so the application can access it.

## How to Use

A newer and improved GUI is currently under development. For now, you can use the existing GUI.

1. Open a terminal in the project directory.
2. Run the application using Python 3:

```bash
python3 GUI.py
```

3. Enter your proxy URL.
4. Click the **Add** button.
5. Select at least one proxy configuration.
6. Click the **Connect** button to connect.

## Supported Proxy Protocols

The application currently supports the following proxy protocols:

* VLESS
* VMess
* Shadowsocks
* Trojan
* Hysteria2
* HTTP
* HTTPS

Make sure the proxy URL you enter uses one of these supported protocols.

## Important Notes

* Add proxy URLs **one at a time**.
* Do not paste multiple proxy URLs at once.
* Do not manually enter Xray/V2Ray configuration settings into the application.
* The current GUI is designed to accept proxy URLs individually.
* To connect, you must select at least one proxy configuration before clicking the **Connect** button.

Entering multiple URLs at once or manually entering raw configuration settings may not work correctly.

## Upcoming GUI

The current GUI will soon be replaced by a newer and improved version with:

* Better user experience
* More control over proxy configurations
* Improved interface and usability
* Additional proxy management features

When the new GUI is ready, the files will be renamed as follows:

```text
GUI.py       → OldGUI.py
betterGUI.py → GUI.py
```

The improved GUI will then become the default interface for the project.

## Project Status

This project is still under development, and some features may change or improve over time.

