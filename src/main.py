import triple

# TODO: Changeable vk_api_version
# default vk_api_version is 5.131
tr = triple.Triple(
    vk_token="Token here",  # Default None
    tg_token="Token here",  # Default None
    ds_token="Token here",  # Default None
    prefix="/",  # default '.'
    config_path="./config/polling.json"  # Default './config/polling.json'. This mean <project_folder>/config/polling.json'.
)


# TODO: regex
@tr.on_message("echo")
def echo(event_type: str, event: triple.types.MessageObject):
    """ example """

    # Triggered from '.echo'

    # Available event_types:
    # tg_event
    # vk_event
    # ds_event

    return f"Event type: `{event_type}`\n\nMessage: `{event.text}`\n\nEvent: `{event!r}`"


if __name__ == '__main__':
    tr.run()
