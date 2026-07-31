# Digital Guardian ARC

Publisher: Digital Guardian <br>
Connector Version: 3.0.0 <br>
Product Vendor: Digital Guardian <br>
Product Name: Digital Guardian <br>
Minimum Product Version: 4.9.39220

This App integrates with Digital Guardian ARC to provide various ingestion and investigative actions

### Configuration variables

This table lists the configuration variables required to operate Digital Guardian ARC. These variables are specified when configuring a Digital Guardian asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**auth_url** | required | string | Authorization Server |
**arc_url** | required | string | ARC URL |
**client_id** | required | string | Client ID |
**client_secret** | required | password | Client Secret |
**export_profile** | required | string | Export Profile GUID |
**verify_server_cert** | optional | boolean | Verify TLS certificates presented by Digital Guardian ARC and the local SOAR server |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration <br>
[add watchlist entry](#action-add-watchlist-entry) - Add an entry to ARC Watchlist <br>
[remove watchlist entry](#action-remove-watchlist-entry) - Remove an entry from ARC Watchlist <br>
[check watchlist entry](#action-check-watchlist-entry) - Check for an entry in ARC Watchlist <br>
[add componentlist entry](#action-add-componentlist-entry) - Add an entry to Componentlist <br>
[remove componentlist entry](#action-remove-componentlist-entry) - Remove an entry from Componentlist <br>
[check componentlist entry](#action-check-componentlist-entry) - Check for an entry in Componentlist <br>
[on poll](#action-on-poll) - Ingest alerts from ARC into Phantom as events

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'add watchlist entry'

Add an entry to ARC Watchlist

Type: **correct** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_name** | required | Watchlist Name | string | `digitalguardianarc watchlist name` |
**watchlist_entry** | required | Entry value to be added to ARC Watchlist | string | `digitalguardianarc watchlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.watchlist_name | string | `digitalguardianarc watchlist name` | Global - Webmail Domains |
action_result.parameter.watchlist_entry | string | `digitalguardianarc watchlist entry` | abc.exe |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully added abc.exe to watchlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'remove watchlist entry'

Remove an entry from ARC Watchlist

Type: **contain** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_name** | required | Watchlist Name | string | `digitalguardianarc watchlist name` |
**watchlist_entry** | required | Entry value to be removed from ARC Watchlist | string | `digitalguardianarc watchlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.watchlist_name | string | `digitalguardianarc watchlist name` | Global - Webmail Domains |
action_result.parameter.watchlist_entry | string | `digitalguardianarc watchlist entry` | abc.exe |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully removed abc.exe from watchlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'check watchlist entry'

Check for an entry in ARC Watchlist

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_name** | required | Watchlist Name | string | `digitalguardianarc watchlist name` |
**watchlist_entry** | required | Entry value to be checked in ARC Watchlist | string | `digitalguardianarc watchlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.watchlist_name | string | `digitalguardianarc watchlist name` | Global - Webmail Domains |
action_result.parameter.watchlist_entry | string | `digitalguardianarc watchlist entry` | abc.exe |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully found abc.exe in watchlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'add componentlist entry'

Add an entry to Componentlist

Type: **correct** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist_name** | required | Componentlist Name | string | `digitalguardianarc componentlist name` |
**componentlist_entry** | required | Entry value to be added to Componentlist | string | `digitalguardianarc componentlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.componentlist_name | string | `digitalguardianarc componentlist name` | Global - Webmail Domains |
action_result.parameter.componentlist_entry | string | `digitalguardianarc componentlist entry` | abc.com |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully added abc.com to componentlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'remove componentlist entry'

Remove an entry from Componentlist

Type: **contain** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist_name** | required | Componentlist Name | string | `digitalguardianarc componentlist name` |
**componentlist_entry** | required | Entry value to be removed from Componentlist | string | `digitalguardianarc componentlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.componentlist_name | string | `digitalguardianarc componentlist name` | Global - Webmail Domains |
action_result.parameter.componentlist_entry | string | `digitalguardianarc componentlist entry` | abc.com |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully removed abc.com from componentlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'check componentlist entry'

Check for an entry in Componentlist

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist_name** | required | Componentlist Name | string | `digitalguardianarc componentlist name` |
**componentlist_entry** | required | Entry value to be checked in Componentlist | string | `digitalguardianarc componentlist entry` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.componentlist_name | string | `digitalguardianarc componentlist name` | Global - Webmail Domains |
action_result.parameter.componentlist_entry | string | `digitalguardianarc componentlist entry` | abc.com |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | Successfully found abc.com in componentlist=Global - Webmail Domains |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'on poll'

Ingest alerts from ARC into Phantom as events

Type: **ingest** <br>
Read only: **True**

The default start_time is the past 5 days and the default end_time is now.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** | optional | Container IDs to limit the ingestion to | string | |
**start_time** | optional | Start of time range, in epoch time (milliseconds) | numeric | |
**end_time** | optional | End of time range, in epoch time (milliseconds) | numeric | |
**container_count** | optional | Maximum number of container records to query for | numeric | |
**artifact_count** | optional | Maximum number of artifact records to query for | numeric | |

#### Action Output

No Output

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
