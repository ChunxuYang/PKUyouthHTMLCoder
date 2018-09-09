#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: run.py

__author__ = "Rabbit"
__version__ = "1.0.3"


import sys
sys.path.append('../lib/')

import os
from datetime import datetime
from optparse import OptionParser, OptionGroup

from util import Config
from coder import HTMLCoder
from error import NoDocxFileError


Root_Dir = os.path.join(os.path.dirname(__file__), '../')   # 项目根目录
Static_Dir = os.path.join(Root_Dir, "static/")              # 静态文件夹
Project_Dir = os.path.join(Root_Dir, "project/")            # 工程文件夹
Build_Dir = os.path.join(Project_Dir, 'build/')             # 输出文件夹


def __get_docx_file(folder=Project_Dir):
	""" 返回目标文件夹下修改日期最新的 docx 文件路径

		Args:
			folder    str    目标文件夹路径，此处即为工程文件夹路径
		Returns:
			file      str    docx 文件路径
		Raises:
			NoDocxFileError  未找到任何 docx 文件
	"""
	for file in sorted(os.listdir(folder), key=lambda file: os.path.getmtime(file), reverse=True):
		if not os.path.isdir(file) and os.path.splitext(file)[1] == '.docx':
			return file
		else:
			continue
	raise NoDocxFileError('*.docx file is missing in %s !' % os.path.abspath(folder))


def main(**kwargs):

	htmlcoder = HTMLCoder(file=__get_docx_file(), output=Build_Dir, **kwargs)
	htmlcoder.work()

	with open(os.path.join(Static_Dir, "preview.template.html"), "r", encoding="utf-8") as rfp:
		with open(os.path.join(Build_Dir, "preview.html"), "w", encoding="utf-8") as wfp:
			wfp.write(rfp.read().format(
				title = htmlcoder.filename,
				src = "./%s.html" % htmlcoder.filename,
				timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
			))


if __name__ == '__main__':

	parser = OptionParser(
		version="HTMLCoder %s" % __version__,
		description="HTMLCoder -- A small tool that can convert a '*.docx' file to a '*.html' file, which is in accord with PKUyouth's style.")

	group_base = OptionGroup(parser,
			title="Base Options")
	group_base.add_option("-s", "--static", dest="static_server_type", metavar="TYPE",
								help="Type of static server. Options: ['Tietuku','SM.MS','Elimage']")

	group_coding_params = OptionGroup(parser,
			title="Parameters of Coding Process",
			description="Or will use default setting from 'config/coder.ini' file.")
	group_coding_params.add_option("--no-reporter", action="store_true", dest="no_reporter",
										help="Whether this article has reporters information or not. (Default: False)")
	group_coding_params.add_option("--no-reference", action="store_true", dest="no_reference",
										help="Whether this article has references or not. (Default: True)")
	group_coding_params.add_option("--count-word", action="store_true", dest="count_word",
										help="Output word's sum. (Default: True)")
	group_coding_params.add_option("--count-picture", action="store_true", dest="count_picture",
										help="Output picture's sum. (Default: False)")

	group_extend_functions = OptionGroup(parser,
			title="Extended Options",
			description="These options may be helpful to you.")
	group_extend_functions.add_option("-e", "--extract-picture", action="store_true", dest="extract_picture",
										help="Extract all pictures to 'project/build/images/' dir in sequence.")

	parser.add_option_group(group_base)
	parser.add_option_group(group_coding_params)
	parser.add_option_group(group_extend_functions)

	options, args = parser.parse_args()


	main(**options.__dict__)

