<!-- vim: tw=72 fo+=a
-->

displace
========

Display placer -- an Xorg-supporting tool to **automatically place your
displays in a way you prefer**, replacing KDE, GNOME or manual calls to
`xrandr`. Similar¹ to <a
href="https://github.com/phillipberndt/autorandr ">autorandr</a>.

You know that problem. You've got your <a
href="https://github.com/dpiegdon/qtile-setup">fancy tiling window
manager set up</a> exactly the way you like it, and you use that
configuration across all of your computers. On your desktop, laptop and
office PC, with docking station or without, and also when giving random
presentations all alone in homeoffice...

But you *really* don't want to use some desktop environment like KDE or
GNOME or whatever, because why the hell! On the other hand, you don't
want to remember `xrandr` commands all the time, or have an
xrandr-script per setup.

Thats where `displace` comes in:

**Python-native²** tool that **scans** which **output ports** exist,
which **monitors** are connected, and which of the known configurations
are **possible given this hardware**. Either list them, pick one, or let
`displace` pick the one with the highest priority. Supports executing
extra commands depending on the selected setup, like changing your DPI
configuration, or restarting your windowmanager.

configuration
-------------

For now, configuration is hard-coded in `config.py` using helpers from
`cfghelper.py`.

A `DesktopSetup` or `DESK` is a full configuration for monitors
connected to the output ports of your computer. You can have multiple of
those. `displace` will show you which of those are possible given
currently connected hardware, and let you pick one.

Each `DesktopSetup` consists of one or multiple `OutputSetup` or `OUT`.
An `OutputSetup` configures a single, existing output. You can reference
it by output port name (like "DVI-0", "VGA-0", ... -- those, that
`xrandr` shows) or by a monitor name, derived from the monitors EDID.
Part of a `DesktopSetup` is also a specific `postexec` list -- commands
to be executed when picking this configuration and applying it.

To see currently connected output ports and monitors, check the output
of `displace` or `displace -v`. `--verbose` shows additional names that
are also available for your monitor, which may help when the primary
name is not unique. `--veryverbose` or `-V` shows even more info.

The **ultimate configuration** of `displace` is defined by
`defined_setups` and `postexec_all` in `config.py`. `defined_setups` is
a list of `DesktopSetup` instances, while `postexec_all` is a list of
commands to be executed after any change of the monitor setup.

For an example, just see `config.py`.

smallprint
----------

¹ Well, somewhat. Only in principle.

² Working on it: xlib-calls to read status information are already using
python-xlib, but XRANDR configuration of displays are still done by
executing `xrandr` commands, not using python-xlib yet.
