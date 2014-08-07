import os
import csv
import zipfile


class Writer:

    def __init__(self):
        pass

    def write(self, locality_name, businesses, export_dir=os.path.join(os.path.dirname(__file__), 'export')):
        """
        :param locality_name : string
        :param businesses : list[Business]
        :param export_dir : string
        """
        # make a file name from the locality name
        file_name = locality_name.title().replace(" ", "_")

        self._set_up(file_name, export_dir)
        with open(self.businesses_path_tmp, 'w') as businesses_csv, \
                open(self.inspections_path_tmp, 'w') as inspections_csv:

            business_writer = csv.writer(businesses_csv)
            inspection_writer = csv.writer(inspections_csv)

            for business in businesses:
                business_writer.writerow([business.business_id, business.name, business.address])
                for inspection in business.inspections:
                    inspection_writer.writerow([business.business_id, inspection.date])

        # add CSVs to zip archive
        self.zip_file.write(self.businesses_path_tmp, os.path.join(file_name, 'businesses.csv'))
        self.zip_file.write(self.inspections_path_tmp, os.path.join(file_name, 'inspections.csv'))


    def _set_up(self, file_name, export_dir):

        # build temp file paths
        tmp_dir = os.path.join(export_dir, 'tmp')
        self.businesses_path_tmp = os.path.join(tmp_dir, file_name + '_businesses.csv')
        self.inspections_path_tmp = os.path.join(tmp_dir, file_name + '_inspections.csv')

        # create filesystem dir if need be
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            os.makedirs(tmp_dir)

        # initialize a zip archive
        archive_file = os.path.join(export_dir, file_name + ".zip")
        self.zip_file = zipfile.ZipFile(archive_file, "w")

    def _tear_down(self):
        # delete tmp files
        os.remove(self.businesses_path_tmp)
        os.remove(self.inspections_path_tmp)


