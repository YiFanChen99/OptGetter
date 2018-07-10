#!/usr/bin/python

import getopt
import unittest


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


class MyTestOptGetter(OptGetter):
    options = "hf:o:r"
    help_message = "usage: Getter [-h] [-f F_PARAM] [-o O_PARAM] [-r]"

    def __init__(self):
        options = MyTestOptGetter.options
        help_message = MyTestOptGetter.help_message
        super(MyTestOptGetter, self).__init__(options=options, help_message=help_message)


class OptGetterTest(unittest.TestCase):

    def setUp(self):
        self.getter = MyTestOptGetter()

    def tearDown(self):
        self.getter = None

    def test_empty_argv(self):
        argv = []
        options, arguments = self.getter.get(argv)
        self.assertEqual([], options)
        self.assertEqual([], arguments)

    def test_only_one_empty_string(self):
        argv = "".split(' ')
        options, arguments = self.getter.get(argv)
        self.assertEqual([], options)
        self.assertEqual([""], arguments)

    def test_h_anywhere(self):
        with self.assertRaises(OptHelpError):
            argv = "-h".split(' ')
            options, arguments = self.getter.get(argv)

        with self.assertRaises(OptHelpError):
            argv = "-h -f file_path -r".split(' ')
            options, arguments = self.getter.get(argv)

        with self.assertRaises(OptHelpError):
            argv = "-f file_path -r -h".split(' ')
            options, arguments = self.getter.get(argv)

    def test_help_message(self):
        """
        The error message from OptHelpError is the help_message.
        """
        defined_message = MyTestOptGetter.help_message
        with self.assertRaises(OptHelpError) as help_error:
            argv = "-h".split(' ')
            options, arguments = self.getter.get(argv)
        self.assertEqual(defined_message, str(help_error.exception))

    def test_invalid_wrong_options(self):
        with self.assertRaises(OptInvalidError):
            argv = "-s".split(' ')
            options, arguments = self.getter.get(argv)

        with self.assertRaises(OptInvalidError):
            argv = "-f ekko_file.so -s".split(' ')
            options, arguments = self.getter.get(argv)

    def test_invalid_option_without_argument(self):
        with self.assertRaises(OptInvalidError):
            argv = "-f".split(' ')
            options, arguments = self.getter.get(argv)

    def test_invalid_message(self):
        with self.assertRaises(OptInvalidError) as invalid_error:
            argv = "-s".split(' ')
            options, arguments = self.getter.get(argv)
        self.assertEqual("Invalid parameters. option -s not recognized", str(invalid_error.exception))

    def test_full_argv(self):
        argv = "-f file.so -o fuji -r u eiki".split(' ')
        options, arguments = self.getter.get(argv)
        self.assertEqual([('-f', "file.so"), ('-o', "fuji"), ('-r', "")], options)
        self.assertEqual(["u", "eiki"], arguments)

    def test_too_many_arguments(self):
        argv = "-f file1.so file2.so -o fuji".split(' ')
        options, arguments = self.getter.get(argv)
        self.assertEqual([('-f', "file1.so")], options)
        self.assertEqual(["file2.so", "-o", "fuji"], arguments)


if __name__ == "__main__":
    unittest.main()
