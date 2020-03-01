# -*- coding: utf-8 -*-


import logging

import {{cookiecutter.project_slug}}

def init_logging():
    log_str = "[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)d %(message)s "
    logging.basicConfig(
        format=log_str,
        level=logging.DEBUG,
        filename='{{cookiecutter.project_slug}}.log',
        datefmt='%m/%d/%Y %I:%M:%S%p',
    )

if __name__ == "__main__":
    init_logging()

    print("Hello!")
