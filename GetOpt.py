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
        """
        options_in_dict:
            False: Return options in type tuple(pair)-in-list. (orderly)
            True : Return options in type dict. (disorder)
        """
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


class _MyTestOptGetter(OptGetter):
    options = "hf:o:r"
    help_message = "usage: Getter [-h] [-f F_PARAM] [-o O_PARAM] [-r]"

    def __init__(self):
        options = _MyTestOptGetter.options
        help_message = _MyTestOptGetter.help_message
        super(_MyTestOptGetter, self).__init__(options=options, help_message=help_message)


class _OptGetterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.getter = _MyTestOptGetter()

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
        defined_message = _MyTestOptGetter.help_message
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


class _OptGetterArgOptionsInDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.getter = _MyTestOptGetter()
        cls.argv = "-f file.so -f lastF -r u eiki".split(' ')

    def assertEqualCorrespondingToArg(self, **kwargs):
        options_expected = kwargs.pop('options_expected')

        options, arguments = self.getter.get(self.argv, **kwargs)

        self.assertEqual(options_expected, options)
        self.assertEqual(["u", "eiki"], arguments)

    def test_arg_is_false(self):
        options_expected = [('-f', "file.so"), ('-f', "lastF"), ('-r', "")]
        self.assertEqualCorrespondingToArg(options_in_dict=False, options_expected=options_expected)

    def test_arg_is_true(self):
        options_expected = {'-f': "lastF", '-r': ""}
        self.assertEqualCorrespondingToArg(options_in_dict=True, options_expected=options_expected)

    def test_arg_is_default_false(self):
        options_expected = [('-f', "file.so"), ('-f', "lastF"), ('-r', "")]
        self.assertEqualCorrespondingToArg(options_expected=options_expected)


if __name__ == "__main__":
    unittest.main()
