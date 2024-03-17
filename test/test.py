from pathlib import Path


def tree(path='.', head='', tail=''):
    path = Path(path)

    if path.is_dir():
        print(path.name)
        entries = sorted(filter(Path.is_dir, path.iterdir()))
        print(entries)

        # for i, entry in enumerate(entries):
        #     if i < len(entries) - 1:
        #         tree(entry, tail + '├──', tail + '│  ')
        #     else:
        #         tree(entry, tail + '└──', tail + '   ')

tree('D:\\test')
