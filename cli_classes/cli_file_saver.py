from cli_classes.cli_caller import CliCaller
from io import BytesIO
import gzip


class CliFileSaver(CliCaller):

    def save_files(self):
        if self.api_object.request_method_name == self.api_object.CONST_REQUEST_METHOD_GET:
            file_type = self.api_object.params['type']
        else:
            file_type = self.api_object.data['type']

        api_response = self.api_object.api_response

        # some older webservice instances won't have that header
        if 'Vx-Filename' in self.api_object.api_response.headers:
            filename = '{}_{}'.format(self.given_args['sha256'], self.api_object.api_response.headers['Vx-Filename'])
        else:
            filename = '{}.{}'.format(self.given_args['sha256'], file_type)

        f_out_name = self.cli_output_folder + '/' + filename
        if file_type == 'memory':
            f_out_name += '.zip'

        if file_type in ['xml', 'html', 'bin', 'pcap']:
            f_out = open(f_out_name, 'wb')
            try:
                gzip_file_handle = gzip.GzipFile(fileobj=BytesIO(api_response.content))
                f_out.write(gzip_file_handle.read())
            except Exception as e:
                f_out = open(f_out_name, 'wb')
                f_out.write(api_response.content)
                f_out.close()
            f_out.close()
        else:
            f_out = open(f_out_name, 'wb')
            f_out.write(api_response.content)
            f_out.close()
