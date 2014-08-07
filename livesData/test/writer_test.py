import unittest
import os
from mock import patch
from mock import MagicMock
from livesData import Writer, Business
import zipfile
import pprint

def my_open_side_effect(*args, **kwargs):
    if args[0] == '/mock/path/Norfolk_businesses.csv':
        print 'here'
    elif args[0] == '/mock/path/Norfolk_inspections.csv':
        print 'there'


class WriterTestCase(unittest.TestCase):

    def setUp(self):
        self.writer = Writer()


class WriterSetUpTestCase(WriterTestCase):

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('zipfile.ZipFile')
    def runTest(self, zip_file_mock, makedirs_mock, path_exists_mock):
        # make the path not exist
        path_exists_mock.return_value = False

        self.writer._set_up('Norfolk', '/mock/path')

        # assert checks if export paths exist
        path_exists_mock.assert_called_once_with('/mock/path')

        # assert creates paths
        self.assertEquals(2, makedirs_mock.call_count)
        makedirs_mock.assert_any_call('/mock/path')
        makedirs_mock.assert_any_call('/mock/path/tmp')

        # initializes a zip archive for writing
        zip_file_mock.assert_called_once_with('/mock/path/Norfolk.zip', 'w')


class WriterWriteTestCase(WriterTestCase):

    @patch('livesData.Writer._set_up')
    @patch('__builtin__.open')
    @patch('livesData.Writer._tear_down')
    def runTest(self, tear_down_mock, open_mock, set_up_mock):
        # set some props set in set up
        self.writer.businesses_path_tmp = '/mock/path/Norfolk_businesses.csv'
        self.writer.inspections_path_tmp = '/mock/path/Norfolk_inspections.csv'

        # make open return file mock
        file_mock = open_mock.side_effect = my_open_side_effect

        # mock zip writer
        self.writer.zip_file = MagicMock(spec=zipfile.ZipFile)

        mock_businesses = []
        for mock_id in range(0, 3):
            b = Business(mock_id, 'Name', '500 Botetourt St.')
            b.add_inspection('20140628')
            mock_businesses.append(b)

        self.writer.write('Norfolk', mock_businesses)








    # @patch('os.path.exists')
    # @patch('os.makedirs')
    # @patch('zipfile.ZipFile')
    # @patch('__builtin__.open')
    # @patch('csv.writer')
    # @patch('os.remove')
    # def runTest(self, os_remove_mock, open_mock, zip_file_mock, makedirs_mock, path_exists_mock):
    #     # make the path not exist
    #     path_exists_mock.return_value = False
    #
    #     # make open return file mock
    #     # file_mock = open_mock.return_value = MagicMock(spec=file)
    #
    #     zip_file_mock.return_value = MagicMock()
    #
    #     mock_businesses = []
    #
    #     for mock_id in range(0, 3):
    #         b = Business(mock_id, 'Name', '500 Botetourt St.')
    #         b.add_inspection('20140628')
    #         mock_businesses.append(b)
    #
    #     self.writer.write(mock_businesses)
    #
    #     # checks if export paths exist
    #     path_exists_mock.assert_called_once_with('/mock/path')
    #
    #     # creates paths
    #     self.assertEquals(2, makedirs_mock.call_count)
    #     makedirs_mock.assert_any_call('/mock/path')
    #     makedirs_mock.assert_any_call('/mock/path/tmp')
    #
    #     # initializes a zip archive for writing
    #     zip_file_mock.assert_called_once_with('/mock/path/Norfolk.zip', 'w')
    #
    #     # opens files
    #     self.assertEquals(2, open_mock.call_count)
    #     open_mock.assert_any_call('/mock/path/tmp/Norfolk_businesses.csv', 'w')
    #     open_mock.assert_any_call('/mock/path/tmp/Norfolk_inspections.csv', 'w')





#         @patch('os.path.exists', return_value=False)
# @patch('os.makedirs')
# @patch('zipfile.ZipFile')
# def conTest(self, zip_file_mock, makedirs_mock, path_exists_mock):
#     Writer('Norfolk')
#
#     assert 1 == path_exists_mock.call_count
#     path_exists_mock.return_value = False
#
#     assert 2 == makedirs_mock.call_count
#
#     assert 1 == zip_file_mock.call_count

