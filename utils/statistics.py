r"""
Execute the following commands:
cd ..
(for po in `find . -name "*.po"` ; do echo -n "$po:"; LANG=en msgfmt -o /dev/null --statistics $po 2>&1 |tail -n1; done) > raw_numbers.txt
cd utils
python statistics.py ../raw_numbers.txt
or if you want only your language to be displayed, here french:
python statistics.py ../raw_numbers.txt fr

Number of languages above 70 %:
python statistics.py /tmp/results.txt > /tmp/res
grep -e " ([789][0-9]\." -e " (100\." /tmp/res |wc -l

"""

import os
import sys


DOMAINS = (
    "atcontenttypes",
    "atreferencebrowserwidget",
    "cmfeditions",
    "cmfplacefulworkflow",
    "passwordresettool",
    "plone",
    "plonefrontpage",
    "plonelocales",
    "widgets",
)

result_file = open(sys.argv[1])

stats = {}
for line in result_file:
    path, res = line.split(":")
    language = path.split("/")[-3].replace("_", "-")
    domain = os.path.splitext(os.path.basename(path))[0]
    language = language.lower()
    translated, fuzzy, untranslated = 0, 0, 0
    for part in res.split(","):
        n, mtype, dontcare = part.split()
        if "translated" == mtype:
            translated = int(n)
        if "fuzzy" == mtype:
            fuzzy = int(n)
        if "untranslated" == mtype:
            untranslated = int(n)

    if language not in stats:
        stats[language] = {}
    stats[language][domain] = (translated, fuzzy, untranslated)

result_file.close()

# from pprint import pprint
# pprint(stats)

print("Number of languages: %d" % len(stats))
print("Legend: translated (percentage) / fuzzy / untranslated = total")

lg = None
if len(sys.argv) > 2:
    lg = sys.argv[2]

for language, domains in stats.items():
    if lg is not None and lg != language:
        continue

    total = [0, 0, 0]
    details = ""
    for domain in DOMAINS:
        if domain not in domains:
            details += "\t/!\\ %s file missing\n" % domain
            continue

        values = domains[domain]
        total[0] += values[0]
        total[1] += values[1]
        total[2] += values[2]
        sum_values = sum(values)
        details += "\t%s: %d/%d/%d = %d\n" % (
            domain,
            values[0],
            values[1],
            values[2],
            sum_values,
        )
        if sum_values != sum(
            stats["fr"][domain]
        ):  # French language has all po files, so this is our reference
            details += "\t/!\\ %s NOT SYNCHRONISED\n" % domain

    sum_total = sum(total)
    if sum_total == 0:
        percent = 0.0
    else:
        percent = round(float(total[0]) / float(sum_total) * 100.0, 2)

    print(
        "%s\t: %d (%.2f%%) / %d / %d = %d"
        % (language, total[0], percent, total[1], total[2], sum_total)
    )
    print(details)
