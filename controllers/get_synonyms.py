"""Get synonyms from the target word.

This module gets target word to find synonyms, and returns corresponding synonyms.

Example:
    $ get_synonyms.py [-h] [-n NUMBER] target
"""

import argparse

from nltk.corpus import wordnet


def get_candidates(body):
    """Get candiate words form the body

    This function assume that body is from academic paper, it handle some words which
    don't need to get synonyms. Handling cases are as belows:
    1) reference e.g. [1]
    2) numeric values

    Args:
        body (string): Target content to get candidate words, it can be sentences or paragraphs.

    Returns:
        candidates:
    """
    tkns = body.split(' ')
    tkns_uniq = list(dict.fromkeys(tkns))
    for i, tkn in enumerate(tkns_uniq):
        if '.' in tkn:
            tkns_uniq[i] = tkn.replace('.', '')
    candidates = [tkn for tkn in tkns_uniq
                  if '[' not in tkn and ']' not in tkn and not any(c.isdigit() for c in tkn)]
    if '\n' in candidates:
        candidates.remove('\n')

    return candidates


def get_synonyms_wordnet(target, num=None):
    """Get synonyms from wordnet

    Args:
        target (string): Target word to get synonyms.
        num (int): The number of the synonyms to get.

    Returns:
        synonyms (list): List of synonyms
    """
    synonyms = []
    for syn in wordnet.synsets(target):
        for l in syn.lemmas():
            synonyms.append(l.name())
    synonyms = list(dict.fromkeys(synonyms))
    if target in synonyms:
        synonyms.remove(target)
    if num is None or len(synonyms) < num:
        pass
    else:
        synonyms = synonyms[:num]
    return synonyms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str, help="Target word to get synonyms")
    parser.add_argument('-n', '--number', type=int,
                        help="The number of synonyms to get")
    parser.add_argument('-s', '--string', action='store_true',
                        help="The number of synonyms to get")
    args = parser.parse_args()
    syn_map = {}
    if args.string:
        candi = get_candidates(args.target)
        for tkn in candi:
            syn = get_synonyms_wordnet(tkn, 3)
            syn = [s.replace('_', ' ') for s in syn]
            syn_map[tkn] = syn
    else:
        syn_map[args.target] = get_synonyms_wordnet(args.target, args.number)
    print(syn_map)


if __name__ == '__main__':
    main()
