<!-- vim: tw=72 fo+=a
-->

displace
========

Display placer -- an Xorg-supporting tool to **automatically place your
displays in a way you prefer**, replacing KDE, GNOME or manual calls to
*xrandr*. Similar¹ to <a
href="https://github.com/phillipberndt/autorandr ">autorandr</a>.

You know that problem. You've got your <a
href="https://github.com/dpiegdon/qtile-setup">fancy tabbing window
manager set up</a> exactly the way you like, and you use that
configuration across all your workflows. On your desktop, laptop and
your office PC. With your docking station or without, and also when
giving random presentations all alone in your homeoffice...

But you *really* don't want to use some desktop environment like KDE or
GNOME or whatever to manage your setup, because why the hell! On the
other hand, you don't want to remember XRANDR commands all then time, or
have an xrandr-script per setup.

So thats where **displace** comes in:

**Python-native²** tool that **scans** what **output ports** exist,
which **monitors** exist, and check which of your configurations are
**possible with the given hardware**. Either list them, pick one, or let
*displace* pick the one with the highest priority. Supports executing of
extra commands depending on the selected setup, like changing your DPI
configuration, or restaring your windowmanager.

configuration
-------------

For now, configuration is hard-coded as python in `config.py` using
helpers from `cfghelper.py`.

A `DesktopSetup` (DESK) is a full configuration for monitors connected
to the output ports of your computer. You can have multiple of those.
*displace* will show you which of those are possible given currently
connected hardware, and let you pick one.

Each `DesktopSetup` consists of one or multiple `OutputSetup` (OUT). An
`OutputSetup` configures a single, existing output. You can reference it
but output port name (like "DVI-0", "VGA-0", ... -- those, that xrandr
shows) or by a monitor name, derived from the monitors EDID. Part of a
`DesktopSetup` is also a specific `postexec` list -- commands to be
executed when picking this configuration and applying it.

To see currently connected output ports and the conncected monitors (by
their identifying name), check the output of `displace` or `displace
-v`. `--verbose` shows additional names that are also available for your
monitor, which may help when the primary name is not unique.

The **ultimate configuration** of displace is defined by
`defined_setups` and `postexec_all` in `config.py`. `defined_setups` is
a list of `DesktopSetup`, which `postexec_all` is a list of commands to
be executed after any change of the monitor setup.

For an example, just see `config.py`.

smallprint
----------

¹ Well, somewhat. Only in principle.

² Working on it: xlib-calls to read status information are already using
python-xlib, but XRANDR configuration of displays are still done by
executing *xrandr* commands, not using python-xlib yet.
