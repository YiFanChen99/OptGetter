#!/usr/bin/python

import sys
import getopt


class OptGetter(object):

    def __init__(self, options="", long_options=None, **kwargs):
        super(OptGetter, self).__init__()

        self.options = options
        self.long_options = long_options if long_options is not None else []
        self.help_massage = kwargs.get('help_massage', 'options: %s' % options)
        # self.kwargs = kwargs  # For extending

    def get(self, argv, options_in_dict=False):
        super(OptGetter, self).__init__()

        try:
            options, arguments = getopt.getopt(argv, self.options, self.long_options)
        except getopt.GetoptError:
            self.show_parameter_invalid()
            sys.exit(2)

        for key, value in options:
            if key == '-h':
                print self.help_massage
                sys.exit()

        if options_in_dict:
            options = dict(options)

        return options, arguments

    def show_parameter_invalid(self):
        print "Invalid parameters. \n", self.help_massage, "\n"
