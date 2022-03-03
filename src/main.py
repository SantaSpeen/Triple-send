import triple

# TODO: Changeable vk_api_version, list with allowed_events
# default vk_api_version is 5.131
tr = triple.Triple(
    vk_token="Token here",  # Default None
    tg_token="Token here",  # Default None
    ds_token="Token here",  # Default None
    prefix="/",  # default '.'
    config_path="./config/polling.json"
    # Default './config/polling.json'. This mean <project_folder>/config/polling.json'.
)


@tr.on_message("echo")
def bot_echo(event_type: str, event: triple.types.MessageObject):
    """ example """

    # Triggered from '.echo'

    # Available event_types:
    # tg_event
    # vk_event
    # ds_event

    if event_type == "vk_event":
        return f"Event type: {event_type}\n\nMessage: {event.text}\n\nEvent: {event!r}"

    return f"Event type: `{event_type}`\n\nMessage: `{event.text}`\n\nEvent: `{event!r}`"


@tr.on_message("help", regex=True)
def bot_help(event_type: str, event: triple.types.MessageObject):
    pass


@tr.on_event
async def all_events(event_from: str, event):
    print(event_from, event)


if __name__ == '__main__':
    tr.run()
