from triple import Triple, OnlyFrom


tr = Triple()


@tr.on_message("start", only_from=OnlyFrom.all)
def start(event):
    return f"event:\n```json\n{event}\n```"


if __name__ == '__main__':
    tr.run()
