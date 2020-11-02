import sys
import requests
import json
import phantom.app as phantom
from datetime import datetime
from bs4 import BeautifulSoup
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from digitalguardianarc_consts import DG_CLIENT_HEADER, DG_HEADER_URL


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class DigitalGuardianArcConnector(BaseConnector):
    def __init__(self):

        # Call the BaseConnectors init first

        super(DigitalGuardianArcConnector, self).__init__()
        self._state = None
        self._auth_url = None
        self._arc_url = None
        self._client_id = None
        self._client_secret = None
        self._export_profile = None
        self._api_key = None
        self._client_headers = {}

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})
        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR,
                'Empty response and no information in the header'), None)

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error

        status_code = response.status_code
        self.save_progress("{0}".format(response.status_code))

        try:
            self.save_progress("1")
            soup = BeautifulSoup(response.text, 'html.parser')
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
            self.save_progress("1a")
        except Exception, e:
            error_text = 'Cannot parse error details ' + e

        message = '''Status Code: {0}. Data from server:{1}'''.format(
            status_code, error_text)
        self.save_progress("2")

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        self.save_progress("2")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message),
                      None)

    def _process_json_response(self, r, action_result):

        # Try a json parse

        try:
            resp_json = r.json()
        except Exception, e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR,
                    'Unable to parse JSON response. Error: {0}'.format(
                        str(e))), None)

        # Please specify the status codes here

        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json

        message = \
            'Error from server. Status Code: {0} Data from server: {1}'.format(
                r.status_code, r.text.replace(u'{', '{{').replace(u'}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message),
                      None)

    def _process_response(self, response, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails

        try:
            if hasattr(action_result, 'add_debug_data') and \
                    (self.get_action_identifier() != 'get-file' or not 200 <= response.status_code < 399):
                action_result.add_debug_data(
                    {'r_status_code': response.status_code})
                action_result.add_debug_data({'r_text': response.text})
                action_result.add_debug_data({'r_headers': response.headers})
            if 'json' in response.headers.get('Content-Type', ''):
                self.save_progress('action=process_json_response')
                return self._process_json_response(response, action_result)
            if 'html' in response.headers.get('Content-Type', ''):
                self.save_progress('action=process_html_response')
                return self._process_html_response(response, action_result)
            if not response.text:
                self.save_progress('action=process_empty_response')
                return self._process_empty_response(response, action_result)
            message = (
                "Can't process response from server. Status Code: {0} Data from server: {1}"
            ).format(response.status_code,
                     response.text.replace('{', '{{').replace('}', '}}'))
            self.save_progress(('{}').format(message))
            return RetVal(action_result.set_status(phantom.APP_ERROR, message),
                          None)
        except Exception as e:
            exc_tb = sys.exc_info()
            self.save_progress(
                ('exception_line={} {}').format(exc_tb.tb_lineno, e))
            return RetVal(
                action_result.set_status(phantom.APP_ERROR,
                                         ('Error: {}').format(e)), None)

        return

    def _make_rest_call(self, endpoint, action_result, method='get', **kwargs):

        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR,
                                         'Invalid method: {0}'.format(method)),
                resp_json)

        # Create a URL to connect to

        # url = self._arc_url + endpoint
        url = "%s/rest/1.0/%s" % (self._arc_url.strip("/"), endpoint)
        try:
            # auth=(username, password)  # basic authentication
            self.save_progress("Connecting to URL: {0}".format(url))
            r = request_func(url,
                             verify=config.get('verify_server_cert', False),
                             **kwargs)
        except Exception, e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR,
                    'Error Connecting to server. Details: {0}'.format(str(e))),
                resp_json)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param

        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress('Connecting to DG ARC')
        self.requestApiToken()
        self.save_progress('Got API Token')

        # make rest call
        self.save_progress("Client Headers: {0}".format(self._client_headers))
        (ret_val) = \
            self._make_rest_call('watchlists', action_result,
                                 params=None,
                                 headers=self._client_headers)

        if phantom.is_fail(ret_val):

            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here

            self.save_progress('Test Connectivity Failed.')
            return action_result.get_status()

        # Return success

        self.save_progress('Test Connectivity Passed')
        return action_result.set_status(phantom.APP_SUCCESS)

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        # return action_result.set_status(phantom.APP_ERROR,'Action not yet implemented')

    def _handle_on_poll(self, param):
        oldname = ''
        action_result = self.add_action_result(ActionResult(dict(param)))
        response_status, export_list = self.get_export(
            action_result=action_result)
        if phantom.is_fail(response_status):
            self.debug_print('failed poll')
            return action_result.set_status(phantom.APP_ERROR,
                                            action_result.get_message())
        if export_list:
            self.save_progress('Ingesting data')
        else:
            self.save_progress('No export data found')
            return action_result.set_status(phantom.APP_SUCCESS,
                                            action_result.get_message())
        for entry in export_list:
            if not entry['dg_alert.dg_detection_source'] == 'alert' and entry[
                    'dg_tags']:
                comm = entry['dg_alarm_name'].find(',')
                if comm == -1:
                    comm = 100
                name = ('{alarm_name}-{id}').format(
                    alarm_name=entry['dg_alarm_name'][0:comm],
                    id=entry['dg_guid'])
                if name != oldname:
                    container_id = self.create_container(name, entry)
                    oldname = name
                    if container_id:
                        (artifacts_creation_status,
                         artifacts_creation_msg) = self.create_artifacts(
                             alert=entry, container_id=container_id)
                        if phantom.is_fail(artifacts_creation_status):
                            self.debug_print((
                                'Error while creating artifacts for container with ID {container_id}. {error_msg}'
                            ).format(container_id=container_id,
                                     error_msg=artifacts_creation_msg))
                            self._state['first_run'] = False
        return action_result.set_status(phantom.APP_SUCCESS)

    def get_export(self, action_result):
        self.save_progress('Getting ARC Export data')
        self.requestApiToken()
        full_url = self._arc_url + 'export_profiles/' + \
            self._export_profile + '/export_and_ack'
        request_response = requests.post(url=full_url,
                                         headers=self._client_headers,
                                         verify=False)
        request_status = request_response.status_code
        if phantom.is_fail(request_status):
            return (action_result.get_status(), None)
        headerField = []
        jsonText = json.loads(request_response.text)
        if jsonText['total_hits'] == 0:
            return (phantom.APP_SUCCESS, None)
        for field in jsonText['fields']:
            headerField.append(field['name'])
        exportdata = []
        for data in jsonText['data']:
            entryLine = {}
            headerPosition = 0
            for dataValue in data:
                entryLine[headerField[headerPosition]] = dataValue
                headerPosition += 1
            exportdata.append(entryLine)
        return (phantom.APP_SUCCESS, exportdata)

    def create_container(self, name, items):
        container_dict = dict()
        if not items['dg_alert.dg_detection_source'] == 'alert' and items[
                'dg_tags']:
            container_dict['name'] = name
            container_dict['start_time'] = ('{time}Z').format(
                time=datetime.utcfromtimestamp(items['dg_processed_time'] / 1000).isoformat())
            container_dict['source_data_identifier'] = container_dict['name']
            container_dict['severity'] = self.convert_to_phantom_severity(
                items['dg_alarm_sev'])
            custom_fields = {
                'threat type': (items['dg_tags']),
                'activity': (items['dg_utype'])
            }
            container_dict['tags'] = [('{}={}').format(x, custom_fields[x])
                                      for x in custom_fields
                                      if custom_fields[x] is not None]
            container_creation_status, container_creation_msg, container_id = self.save_container(
                container=container_dict)
            if phantom.is_fail(container_creation_status):
                self.save_progress((
                    'Error while creating container for alert {alert_name}. {error_message}'
                ).format(alert_name=items['dg_alarm_name'],
                         error_message=container_creation_msg))
                return
            else:
                return container_id

    def create_artifacts(self, alert, container_id):
        """ This function is used to create artifacts in given container using export data.

        :param alert: Data of single export
        :param container_id: ID of container in which we have to create the artifacts
        :return: status(success/failure), message
        """

        artifacts_list = []
        cat = 'alarm'
        # self.save_progress(('action=create_artifacts tenant={} artifact={}').format(self._client_id, json.dumps(alert)))
        operation_mapping = {
            'File': ['Alarm', 'Process', 'Computer', 'User', 'File'],
            'CD/D': ['Alarm', 'Process', 'Computer', 'User', 'File'],
            'Netw':
            ['Alarm', 'Process', 'Computer', 'User', 'File', 'Network'],
            'Send': ['Alarm', 'Process', 'Computer', 'User', 'Email'],
            'Proc': ['Alarm', 'Process', 'Computer', 'User'],
            'Appl': ['Alarm', 'Process', 'Computer', 'User'],
            'ADE ': ['Alarm', 'Process', 'Computer', 'User', 'File'],
            'Prin':
            ['Alarm', 'Process', 'Computer', 'User', 'File', 'Network'],
            'Othe': ['Alarm']
        }
        artifacts_mapping = {
            'Alarm': {
                'Alarm_Name': ('dg_alarm_name', []),
                'Alarm_Severity': ('dg_alarm_sev', []),
                'Threat_Type': ('dg_tags', []),
                'Detection_Name': ('dg_det_name', []),
                'Alert_Category': ('dg_alert.dg_category_name', []),
                'Policy_Name':
                ('dg_alert.dg_alert.dg_alert.dg_policy.dg_name', []),
                'Action_Was_Blocked': ('dg_alert.dg_hc', []),
                'startTime': ('dg_local_timestamp', [])
            },
            'File': {
                'File_Name': ('dg_src_file_name', ['fileName']),
                'File_Size': ('dg_alert.dg_total_size', ['fileSize']),
                'File_Was_Classified': ('dg_hc', []),
                'File_Type': ('dg_src_file_ext', ['fileType']),
                'File_Path': ('dg_alert.uad_sp', ['filePath']),
                'Destination_File_Path': ('dg_alert.uad_dp', ['filePath'])
            },
            'Process': {
                'Process_Name': ('dg_proc_file_name', ['process name']),
                'Parent_Process_Name': ('dg_parent_name', ['app']),
                'Process_Path': ('pi_fp', ['filePath']),
                'Command_Line': ('pi_cmdln', []),
                'MD5': ('dg_md5', ['filehash']),
                'SHA1': ('dg_sha1', ['filehash']),
                'SHA256': ('dg_sha256', ['filehash']),
                'VirusTotal_Status': ('dg_vt_status', [])
            },
            'Email': {
                'Attachment_File_Name':
                ('dg_attachments.dg_src_file_name', ['fileName']),
                'Attachment_Was_Classified': ('dg_attachments.uad_sfc', []),
                'Email_Subject': ('ua_msb', ['email']),
                'Email_Sender': ('ua_ms', ['email']),
                'Email_Recipient': ('dg_recipients.uad_mr', ['email']),
                'Email_Recipient_Domain':
                ('dg_recipients.dg_rec_email_domain', ['domain'])
            },
            'Network': {
                'Destination_Address': ('ua_ra', ['ip', 'ipv4']),
                'Request_URL': ('ua_up', ['url']),
                'Destination_DNS_Domain': ('ua_hn', ['domain']),
                'Remote_Port': ('ua_rp', ['ip'])
            },
            'Computer': {
                'Computer_Name': ('dg_machine_name', ['hostname']),
                'Computer_Type': ('dg_machine_type', []),
                'Source_Host_Name': ('dg_shn', []),
                'Source_IP': ('ua_sa', ['ip', 'ipv4']),
                'Source_Address': ('ua_sa', ['ip', 'ipv4'])
            },
            'User': {
                'User_Name': ('dg_user', ['suser']),
                'NTDomain': ('ua_dn', [])
            }
        }
        specific_alert_mapping = {
            'alarm': {
                'dgarcUID': ('dg_guid', []),
                'dg_process_time': ('dg_process_time', []),
                'Activity': ('dg_utype', []),
                'os_version': ('os_version', []),
                'Policy': ('dg_alert.dg_policy.dg_name', []),
                'Printer_Name': ('uad_pn', []),
                'os': ('os', []),
                'browser': ('browser', []),
                'App_Category': ('appcategory', ['category']),
            }
        }
        for (artifact_name, artifact_keys) in artifacts_mapping.items():
            temp_dict = {}
            cef = {}
            cef_types = {}
            # self.save_progress(('artifact_name={}').format(artifact_name))
            for (artifact_key, artifact_tuple) in artifact_keys.items():
                if alert.get(artifact_tuple[0]):
                    cef[artifact_key] = alert[artifact_tuple[0]]
                    cef_types[artifact_key] = artifact_tuple[1]

            cef['tenant'] = self._client_id
            if cef:
                temp_dict['cef'] = cef
                temp_dict['cef_types'] = cef_types
                temp_dict['name'] = artifact_name
                temp_dict['label'] = artifact_name
                temp_dict['type'] = 'host'
                temp_dict['container_id'] = container_id
                temp_dict['severity'] = self.convert_to_phantom_severity(
                    alert['dg_alarm_sev'])
                temp_dict['source_data_identifier'] = self.create_dict_hash(
                    temp_dict)
                temp_dict['tenant'] = self._client_id

                operation = alert['dg_utype'][:4]
                if operation in operation_mapping.keys():
                    accepted_types = operation_mapping[operation]
                else:
                    accepted_types = operation_mapping['Othe']
                if artifact_name in accepted_types:
                    artifacts_list.append(temp_dict)

        if cat in specific_alert_mapping:
            temp_dict = {}
            cef = {}
            cef_types = {}
            artifact_name = '{} Artifact'.format('Alarm Detail')
            # artifact_name = '{} Artifact'.format(alert.get('dg_alarm_name'))
            for (artifact_key,
                 artifact_tuple) in specific_alert_mapping.get(cat).items():
                if alert.get(artifact_tuple[0]):
                    cef[artifact_key] = alert[artifact_tuple[0]]
                    cef_types[artifact_key] = artifact_tuple[1]
            cef['tenant'] = self._client_id
            if cef:
                temp_dict['cef'] = cef
                temp_dict['cef_types'] = cef_types
                temp_dict['name'] = artifact_name
                temp_dict['label'] = artifact_name
                temp_dict['type'] = 'host'
                temp_dict['container_id'] = container_id
                temp_dict['severity'] = self.convert_to_phantom_severity(
                    alert['dg_alarm_sev'])
                temp_dict['source_data_identifier'] = self.create_dict_hash(
                    temp_dict)
                temp_dict['tenant'] = self._client_id
                artifacts_list.append(temp_dict)

        create_artifact_status, create_artifact_msg, _ = self.save_artifacts(
            artifacts_list)
        if phantom.is_fail(create_artifact_status):
            return (phantom.APP_ERROR, create_artifact_msg)
        return (phantom.APP_SUCCESS, 'Artifacts created successfully')

    def convert_to_phantom_severity(self, dg_severity):
        if dg_severity == 'Critical':
            phantom_severity = 'High'
        elif dg_severity == 'High':
            phantom_severity = 'Medium'
        else:
            phantom_severity = 'Low'
        return phantom_severity

    def create_dict_hash(self, input_dict):
        if not input_dict:
            return
        else:
            try:
                input_dict_str = json.dumps(input_dict, sort_keys=True)
                self.debug_print('Handled exception in _create_dict_hash',
                                 str(input_dict_str))
            except Exception as e:
                print str(e)
                self.debug_print('Handled exception in _create_dict_hash', e)
                return

    def get_watchlist_id(self, watchListName):
        self.requestApiToken()
        action_result = self.add_action_result(
            ActionResult(dict(watchListName)))

        full_url = self._arc_url + 'watchlists/'
        response = requests.get(url=full_url,
                                headers=self._client_headers,
                                verify=False)
        jsonText = json.loads(response.text)
        list_id = ''
        if 200 <= response.status_code <= 299:
            for jText in jsonText:
                if str(jText['display_name']).lower() == watchListName.lower():
                    list_id = jText['name']
                    return (list_id)
        else:
            return action_result.set_status(
                phantom.APP_ERROR, ('Web Response Error: {0}').format(r))

    def _check_watchlist_id(self, watchlist_name, watchlist_entry):
        watch_list_id = self.get_watchlist_id(watchlist_name)
        full_url = self._arc_url + 'watchlists/'
        r = requests.get(url=full_url + watch_list_id + '/values?limit=100000',
                         headers=self._client_headers,
                         verify=False)
        if 200 <= r.status_code <= 299:
            jsonText = json.loads(r.text)
            entryExists = False
            for jText in jsonText:
                if str(jText['value_name']).lower() == watchlist_entry.lower():
                    entryExists = True
                    return (jText['value_id'])
        if not entryExists:
            return ''

    def get_list_id(self, list_name, list_type):
        self.requestApiToken()
        full_url = self._arc_url + 'lists/' + list_type
        r = requests.get(url=full_url,
                         headers=self._client_headers,
                         verify=False)
        jsonText = json.loads(r.text)
        list_id = ""
        if 200 <= r.status_code <= 299:
            for jText in jsonText:
                if str(jText['name']).lower() == list_name.lower():
                    list_id = jText['id']
                    return list_id
        else:
            return ''

    def _add_watchlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        watchlist_name = param['watchlist_name']
        watchlist_entry = param['watchlist_entry']
        msg_string = (watchlist_entry + ' to watchlist=' + watchlist_name)
        # self.save_progress(('Watchlistname={} Watchlistentry={}').format(watchlist_name, watchlist_entry))
        watch_list_id = self.get_watchlist_id(watchlist_name)
        if watch_list_id:
            watch_list_entry_json = '[{"value_name":"' + \
                watchlist_entry + '"}]'
            full_url = self._arc_url + 'watchlists/'
            r = requests.post(url=full_url + watch_list_id + '/values/',
                              data=watch_list_entry_json,
                              headers=self._client_headers,
                              verify=False)
            if 200 <= r.status_code <= 299:
                return (action_result.set_status(phantom.APP_SUCCESS,
                                                 'added ' + msg_string), None)
            else:
                return (action_result.set_status(phantom.APP_ERROR,
                                                 'Failed add ' + msg_string),
                        None)
        return action_result.set_status(
            phantom.APP_ERROR, 'Could not find watch_list = ' + watchlist_name)

    def _remove_watchlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        watchlist_name = param['watchlist_name']
        watchlist_entry = param['watchlist_entry']
        msg_string = (watchlist_entry + ' from watchlist=' + watchlist_name)
        watch_list_id = self.get_watchlist_id(watchlist_name)
        if watch_list_id:
            watch_list_value_id = self._check_watchlist_id(
                watchlist_name, watchlist_entry)
            if watch_list_value_id != '':
                full_url = self._arc_url + 'watchlists/'
                r = requests.delete(url=full_url + watch_list_id + '/values/' + watch_list_value_id,
                                    headers=self._client_headers,
                                    verify=False)
                if 200 <= r.status_code <= 299:
                    return (action_result.set_status(phantom.APP_SUCCESS,
                                                     'removed ' + msg_string),
                            None)
                else:
                    return (action_result.set_status(
                        phantom.APP_ERROR,
                        'Failed to remove ' + msg_string), None)
            else:
                return (action_result.set_status(
                    phantom.APP_ERROR,
                    'Could not find entry ' + msg_string), None)
        else:
            return action_result.set_status(
                phantom.APP_ERROR,
                'Could not find watch_list = ' + watchlist_name)

    def _check_watchlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        watchlist_name = param['watchlist_name']
        watchlist_entry = param['watchlist_entry']
        msg_string = (watchlist_entry + ' from watchlist=' + watchlist_name)
        watch_list_id = self.get_watchlist_id(watchlist_name)
        if watch_list_id:
            watch_list_value_id = self._check_watchlist_id(
                watchlist_name, watchlist_entry)
            if watch_list_value_id != '':
                return (action_result.set_status(phantom.APP_SUCCESS,
                                                 'Found ' + msg_string), None)
            else:
                return (action_result.set_status(
                    phantom.APP_SUCCESS,
                    'Failed to find entry ' + msg_string), None)
        else:
            return action_result.set_status(
                phantom.APP_ERROR,
                'Could not find watch_list = ' + watchlist_name)

    def _add_componentlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        componentlist_name = param['componentlist_name']
        componentlist_entry = param['componentlist_entry']
        msg_string = componentlist_entry + \
            ' to componentlist=' + componentlist_name
        list_id = self.get_list_id(componentlist_name, 'component_list')
        self._client_headers["Content-Type"] = "application/json"
        if list_id:
            component_list_entry_json = '{"items":["' + \
                componentlist_entry + '"]}'
            full_url = self._arc_url + 'remediation/lists/'
            r = requests.put(url=full_url + list_id + '/append',
                             headers=self._client_headers,
                             data=component_list_entry_json,
                             verify=False)
            if 200 <= r.status_code <= 299:
                return (action_result.set_status(phantom.APP_SUCCESS,
                                                 'added ' + msg_string), None)
            else:
                return (action_result.set_status(
                    phantom.APP_ERROR,
                    'Failed add ' + msg_string + ' Return Status ' + r.text),
                    None)
        return action_result.set_status(
            phantom.APP_ERROR,
            'Could not find component_list = ' + componentlist_name)

    def _remove_componentlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        componentlist_name = param['componentlist_name']
        componentlist_entry = param['componentlist_entry']
        msg_string = componentlist_entry + \
            ' to componentlist=' + componentlist_name
        list_id = self.get_list_id(componentlist_name, 'component_list')
        self._client_headers["Content-Type"] = "application/json"
        if list_id:
            component_list_entry_json = '{"items":["' + \
                componentlist_entry + '"]}'
            full_url = self._arc_url + 'remediation/lists/'
            r = requests.post(url=full_url + list_id + '/delete',
                              headers=self._client_headers,
                              data=component_list_entry_json,
                              verify=False)
            if 200 <= r.status_code <= 299:
                return (action_result.set_status(phantom.APP_SUCCESS,
                                                 'removed ' + msg_string),
                        None)
            else:
                return (action_result.set_status(
                    phantom.APP_ERROR, 'Failed remove ' + msg_string), None)
        return action_result.set_status(
            phantom.APP_ERROR,
            'Could not find component_list = ' + componentlist_name)

    def _check_componentlist_entry(self, param):
        self.save_progress(('In action handler for: {0}').format(
            self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.debug_print(param)
        componentlist_name = param['componentlist_name']
        componentlist_entry = param['componentlist_entry']
        msg_string = componentlist_entry + \
            ' in componentlist=' + componentlist_name
        list_id = self.get_list_id(componentlist_name, 'component_list')
        if list_id:
            full_url = self._arc_url + 'lists/'
            r = requests.get(url=full_url + list_id + '/values?limit=100000',
                             headers=self._client_headers,
                             verify=False)
            jsonText = json.loads(r.text)
            entryExists = False
            if 200 <= r.status_code <= 299:
                for jText in jsonText:
                    entryExists = True
                    if str(jText['content_value']).lower() == componentlist_entry.lower():
                        return (action_result.set_status(
                            phantom.APP_SUCCESS, 'Found ' + msg_string), None)
            if not entryExists:
                return (action_result.set_status(
                    phantom.APP_SUCCESS,
                    'Failed to find entry ' + msg_string), None)
        else:
            return action_result.set_status(
                phantom.APP_ERROR,
                'Could not find component_list = ' + componentlist_name)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS
        action_id = self.get_action_identifier()
        # self.debug_print('action_id', self.get_action_identifier())
        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'on_poll':
            ret_val = self._handle_on_poll(param)
        elif action_id == 'add_watchlist_entry':
            ret_val = self._add_watchlist_entry(param)
        elif action_id == 'check_watchlist_entry':
            ret_val = self._check_watchlist_entry(param)
        elif action_id == 'remove_watchlist_entry':
            ret_val = self._remove_watchlist_entry(param)
        elif action_id == 'add_componentlist_entry':
            ret_val = self._add_componentlist_entry(param)
        elif action_id == 'remove_componentlist_entry':
            ret_val = self._remove_componentlist_entry(param)
        elif action_id == 'check_componentlist_entry':
            ret_val = self._check_componentlist_entry(param)
        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions

        self.debug_print('action=initialize status=start')
        self._state = self.load_state()
        self.debug_print(('action=initialize state={}').format(self._state))

        config = self.get_config()
        self._auth_url = config['auth_url']
        self._arc_url = config['arc_url']
        self._client_id = config['client_id']
        self._client_secret = config['client_secret']
        self._export_profile = config['export_profile']
        self._client_headers = DG_CLIENT_HEADER
        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades

        # self.save_state(self._state)
        return phantom.APP_SUCCESS

    def validateApiToken(self):

        # if self._api_key == '':
        # return False

        payload = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type':
            'urn:pingidentity.com:oauth2:grant_type:validate_bearer',
            'token': self._api_key,
        }
        api_key_response = requests.post(url=self._auth_url + '/as/introspect.oauth2',
                                         headers=DG_HEADER_URL,
                                         data=payload,
                                         verify=False)
        response_json = api_key_response.json()
        if api_key_response.status_code == 200 and response_json['active']:
            return True
        return False

    def requestApiToken(self):

        if not self.validateApiToken():
            payload = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'client_credentials',
                'scope': 'client',
            }
            api_key_response = requests.post(url=self._auth_url + '/as/token.oauth2',
                                             headers=DG_HEADER_URL,
                                             data=payload,
                                             verify=False)
            response_json = api_key_response.json()

            if api_key_response.status_code == 200:
                self._api_key = response_json['access_token']
                self._client_headers.update(
                    {'Authorization': 'Bearer ' + self._api_key})
                self._client_headers['Authorization'] = 'Bearer ' \
                    + self._api_key
            else:
                return (phantom.APP_ERROR, api_key_response.text)

        else:
            self._client_headers['Authorization'] = 'Bearer ' \
                + self._api_key


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask

        import getpass
        password = getpass.getpass('Password: ')

    if username and password:
        try:
            login_url = \
                DigitalGuardianArcConnector._get_phantom_base_url() \
                + '/login'

            print 'Accessing the Login page'
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print 'Logging into Platform to get the session id'
            r2 = requests.post(login_url,
                               verify=False,
                               data=data,
                               headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception, e:
            print 'Unable to get session id from the platform. Error: ' \
                + str(e)
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print json.dumps(in_json, indent=4)

        connector = DigitalGuardianArcConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print json.dumps(json.loads(ret_val), indent=4)
    exit(0)
