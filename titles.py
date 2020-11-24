#!/usr/bin/env python3

import argparse
import os
import os.path
import re

import toml


def extract_titles(filename, all_languages):
    parsing_frontmatter = True
    parsing_titles = False
    frontmatter = []
    with open(filename) as f:
        content = f.readlines()
        content = content[1:]
        for line in content:
            if parsing_frontmatter:
                if line.strip() == '+++':
                    parsing_frontmatter = False
                    fm = toml.loads(''.join(frontmatter))

                    if 'draft' in fm and fm['draft'] == True:
                        # todo(Gustav): handle drafts better
                        return

                    if all_languages==False and 'english' in fm and fm['english'] == True:
                        return

                    sp = fm['title'].split('-',1)
                    if len(sp)>1:
                        yield sp[1].strip()
                    else:
                        yield sp[0]

                else:
                    frontmatter.append(line)
            else:
                title = line.strip().lower()
                if title.startswith('## titlar') or title.startswith('## titles'):
                    parsing_titles = True
                elif line.strip() == '':
                    parsing_titles = False
                elif parsing_titles:
                    yield line.strip()[2:].strip()


def sort_nicely( key ):
    # from https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    convert = lambda text: int(text) if text.isdigit() else text
    return [convert(c) for c in re.split('([0-9]+)', key)]


def all_episodes(mypath):
    episodes = []
    for f in os.listdir(mypath):
        p = os.path.join(mypath, f)
        if os.path.isfile(p) and os.path.splitext(p)[1] == '.md':
            episodes.append(p)
    episodes.sort(key=lambda x: sort_nicely(x))
    return episodes


def handle_extract_titles(args):
    titles = extract_titles(args.file, args.all)
    for t in titles:
        print(t)


def handle_find_episodes(args):
    episodes = all_episodes(args.folder)
    for e in episodes:
        print(e)


def handle_dump(args):
    episodes = all_episodes(args.folder)
    for ep in episodes:
        for t in set(extract_titles(ep, args.all)):
            print(ep, t)
        print()


def handle_csv(args):
    episodes = []
    for ep in all_episodes(args.folder):
        t = os.path.splitext(os.path.basename(ep))[0]
        episodes.append( (t, len(set(extract_titles(ep, args.all)))) )
    for x in episodes:
        print('"{}",{}'.format(x[0], x[1]))


def handle_all_titles(args):
    for ep in all_episodes(args.folder):
        for t in set(extract_titles(ep, args.all)):
            print(t)


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)

    subs = parser.add_subparsers(help='sub command')

    sub = subs.add_parser('titles')
    sub.add_argument('file')
    sub.add_argument('--all', action='store_true')
    sub.set_defaults(func=handle_extract_titles)

    sub = subs.add_parser('find')
    sub.add_argument('folder')
    sub.set_defaults(func=handle_find_episodes)

    sub = subs.add_parser('dump')
    sub.add_argument('folder')
    sub.add_argument('--all', action='store_true')
    sub.set_defaults(func=handle_dump)

    sub = subs.add_parser('csv')
    sub.add_argument('folder')
    sub.add_argument('--all', action='store_true')
    sub.set_defaults(func=handle_csv)

    sub = subs.add_parser('extract')
    sub.add_argument('folder')
    sub.add_argument('--all', action='store_true')
    sub.set_defaults(func=handle_all_titles)

    args = parser.parse_args()
    if args.func is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
