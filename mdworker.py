import os
from shutil import copyfile
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
import conf
from slugify import slugify
from datetime import datetime

submission_archetype = conf.config["submission"]["archetype_location"]
work_dir = conf.config["git"]["working_dir"]
items_dir = work_dir + "/content/items"


def create(submission):
    title_summary = summarize(submission.title)
    file_tile = slugify(title_summary, separator="_", max_length=25)
    file_location = items_dir + "/" + file_tile + ".md"
    replaces = {
        "!!TITLE_REPLACE!!": str(submission.title),
        "!!DATE_REPLACE!!": str(datetime.utcfromtimestamp(submission.created_utc)),
        "!!ITEMURL_SOCCER_REPLACE!!": str("https://old.reddit.com" + submission.permalink),
        "!!ITEMURL_REPLACE!!": str(submission.url)

    }
    copyfile(submission_archetype, file_location)

    for key in replaces.keys():
        replace_placeholder(file_location, key, replaces[key])

    result = {
        'file_title': file_tile,
        'file_location_relative': file_location,
        'file_location_absolute': os.path.abspath(file_location)
    }

    return result


def replace_placeholder(f, placeholder, text):
    with open(f) as r:
        a = r.read().replace(placeholder, text)
    with open(f, "w") as w:
        w.write(a)


def summarize(text):
    auto_abstractor = AutoAbstractor()
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    auto_abstractor.delimiter_list = [".", "\n"]
    abstractable_doc = TopNRankAbstractor()
    result_dict = auto_abstractor.summarize(str(text), abstractable_doc)
    concat = ""
    for sentence in result_dict["summarize_result"]:
        return sentence
