# titles.py

Extract titles (and alternative titles) from the kodsnack pod.

Make sure you have the episode repo handy.

## Examples

### Extract titles

Extracts all titles, one per line

```bash
titles.py extract ../kodsnack-site/content/avsnitt/ > titles.txt
```

### Dump titles

Dump all titles, with "episode file"

```bash
titles.py dump ../kodsnack-site/content/avsnitt/ > dump.txt
```

```
> cat dump.txt
../kodsnack-site/content/avsnitt/1.md Main title
../kodsnack-site/content/avsnitt/1.md Alternative title

../kodsnack-site/content/avsnitt/1.md Another title
```

### CSV export

Generate a csv file in the form of `name,number of titles`. This is useful for importing into microsoft excel or google sheets and making pretty graphs.

```bash
titles.py csv ../kodsnack-site/content/avsnitt/ > titles.csv
```

### English too?

By default, the script only operates on the swedish titles. Add the --all flag to also operate on *both* swedish *and* english titles.

```bash
titles.py extract ../kodsnack-site/content/avsnitt/ --all > titles.txt
```
