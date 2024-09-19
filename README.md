# DevDeck - Toggl integration

![CI](https://github.com/nicdumz/devdeck-hue/workflows/CI/badge.svg?branch=main)

[Toggl](https://toggl.com) controls for [DevDeck](https://github.com/jamesridgway/devdeck).

## Installing

Simply install _DevDeck - Toggl into the same python environment that you have installed DevDeck.

    pip install devdeck-toggl

You can then update your DevDeck configuration to use decks and controls from this package.

## Controls

- `toggle.Toggle`

  Can be used to toggle on/off a time entry.
  Default behavior toggles the last time entry.
  TODO: extend settings so we define which project/time entry that should be.

## One-time setup

The `toggl` module which is used under the hood requires saving locally an API token for Toggl, once.  Easiest way to do this is:

```
toggl ls
```

Which will bring up a configuration wizard.

## Configuration

Example configuration:

    decks:
      - serial_number: ABC123
        name: devdeck.decks.single_page_deck_controller.SinglePageDeckController
        settings:
          controls:
            - name: devdeck_toggl.toggle.Toggle
              key: 0
