import triple

tr = triple.Triple(
    vk_token="Token here",  # Default None
    tg_token="Token here",  # Default None
    ds_token="Token here",  # Default None
    prefix="/"  # default '.'
)


@tr.on_message("echo")
def start(event_type, event: triple.types.MessageObject):

    return f"Echo: `{event.text}`\n\nEvent:\n```json\n{event.raw}\n```"


if __name__ == '__main__':
    tr.run()
