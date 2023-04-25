from absl import app
from absl import flags

import connector

import gspread
from selenium import webdriver

FLAGS = flags.FLAGS
flags.DEFINE_string('username', '', 'The comicspriceguide username.')
flags.DEFINE_string('password', '', 'The comicspriceguide password.')

url = "https://comicspriceguide.com/Search"

def get_sheet():
    gc = gspread.service_account()
    return gc.open("Comic book index").sheet1

def main(unused_argv):
    del unused_argv

    #comic = connector.Comic(
    #    driver=driver,
    #    username=FLAGS.username,
    #    password=FLAGS.password,
    #    title="The Amazing Spiderman",
    #    issue=12,
    #    year=1964,
    #    url=url,
    #)
    #comic.get()
    comicbook_sheet = connector.Speadsheet(sheet=get_sheet())
    if not comicbook_sheet.parse_sheet():
        print('No comicbooks found in sheet. Exiting.')
        exit(0)
    
    if not comicbook_sheet.unprocessed:
        print('No unprocessed comicbooks found in sheet. Exiting.')
        exit(0)

    driver = webdriver.Chrome()
    for i in range(len(comicbook_sheet.unprocessed)):
        comic = connector.Comic(
            driver=driver,
            username=FLAGS.username,
            password=FLAGS.password,
            title=comicbook_sheet.unprocessed[i][0],
            issue=comicbook_sheet.unprocessed[i][1],
            year=comicbook_sheet.unprocessed[i][2],
            url=url,
        )
        print('Processing comic title: %s issue: %s year: %s' % (
            comic.title, comic.issue, comic.year))
        comic.get()
        comicbook_sheet.unprocessed[i][4] = comic.issue_link
        comicbook_sheet.unprocessed[i][5] = comic.graded_10
        comicbook_sheet.unprocessed[i][6] = comic.ungraded_10
        comicbook_sheet.unprocessed[i][7] = comic.graded_9
        comicbook_sheet.unprocessed[i][8] = comic.ungraded_9
        comicbook_sheet.unprocessed[i][9] = comic.graded_8
        comicbook_sheet.unprocessed[i][10] = comic.ungraded_8
        comicbook_sheet.unprocessed[i][11] = comic.graded_7
        comicbook_sheet.unprocessed[i][12] = comic.ungraded_7
        comicbook_sheet.unprocessed[i][13] = comic.graded_6
        comicbook_sheet.unprocessed[i][14] = comic.ungraded_6
        comicbook_sheet.unprocessed[i][15] = comic.graded_5
        comicbook_sheet.unprocessed[i][16] = comic.ungraded_5
        comicbook_sheet.unprocessed[i][17] = comic.graded_4
        comicbook_sheet.unprocessed[i][18] = comic.ungraded_4
        comicbook_sheet.unprocessed[i][19] = comic.graded_3
        comicbook_sheet.unprocessed[i][20] = comic.ungraded_3
        comicbook_sheet.unprocessed[i][21] = comic.graded_2
        comicbook_sheet.unprocessed[i][22] = comic.ungraded_2
        comicbook_sheet.unprocessed[i][23] = comic.graded_1
        comicbook_sheet.unprocessed[i][24] = comic.ungraded_1
        comicbook_sheet.update_sheet(comicbook_sheet.unprocessed[i])

    

if __name__ == "__main__":
    app.run(main)
