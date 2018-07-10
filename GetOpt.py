#!/usr/bin/python

import getopt


class OptInvalidError(Exception):
    pass


class OptHelpError(Exception):
    pass


class OptGetter(object):

    def __init__(self, options="", long_options=None, **kwargs):
        super(OptGetter, self).__init__()

        self.options = options
        self.long_options = long_options if long_options is not None else []
        self.help_message = kwargs.get('help_message', 'options: %s' % options)
        # self.kwargs = kwargs  # For extending

    def get(self, argv, options_in_dict=False):
        super(OptGetter, self).__init__()

        try:
            options, arguments = getopt.getopt(argv, self.options, self.long_options)
        except getopt.GetoptError as e:
            raise OptInvalidError("Invalid parameters. %s" % str(e))

        for key, value in options:
            if key == '-h':
                raise OptHelpError(self.help_message)

        if options_in_dict:
            options = dict(options)

        return options, arguments

