from absl import app
from absl import flags

import connector

from selenium import webdriver

FLAGS = flags.FLAGS
flags.DEFINE_string('username', '', 'The comicspriceguide username.')
flags.DEFINE_string('password', '', 'The comicspriceguide password.')

url = "https://comicspriceguide.com/Search"

def main(unused_argv):
    del unused_argv

    driver = webdriver.Chrome()
    comic = connector.Comic(
        driver=driver,
        username=FLAGS.username,
        password=FLAGS.password,
        title="The Amazing Spiderman",
        issue=12,
        year=1964,
        url=url,
    )
    comic.get()

    print(comic)

if __name__ == "__main__":
    app.run(main)
