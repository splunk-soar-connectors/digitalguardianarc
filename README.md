[comment]: # "Auto-generated SOAR connector documentation"
# Digital Guardian ARC

Publisher: Digital Guardian  
Connector Version: 2\.0\.1  
Product Vendor: Digital Guardian  
Product Name: Digital Guardian  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This App integrates with Digital Guardian ARC to provide various ingestion and investigative actions

[comment]: # " File: readme.md"
[comment]: # ""
[comment]: # "  Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)"
[comment]: # ""
**Notes**

-   Export GUID

      

    -   You will need to work with the Digital Guardian Services team to get the correct ARC Export
        to support Phantom.

          
          


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Digital Guardian asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**auth\_url** |  required  | string | Authorization Server
**arc\_url** |  required  | string | ARC URL
**client\_id** |  required  | string | Client ID
**client\_secret** |  required  | password | Client Secret
**export\_profile** |  required  | string | Export Profile GUID

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[add watchlist entry](#action-add-watchlist-entry) - Add an entry to ARC Watchlist  
[remove watchlist entry](#action-remove-watchlist-entry) - Remove an entry from ARC Watchlist  
[check watchlist entry](#action-check-watchlist-entry) - Check for an entry in ARC Watchlist  
[add componentlist entry](#action-add-componentlist-entry) - Add an entry to Componentlist  
[remove componentlist entry](#action-remove-componentlist-entry) - Remove an entry from Componentlist  
[check componentlist entry](#action-check-componentlist-entry) - Check for an entry in Componentlist  
[on poll](#action-on-poll) - Ingest alerts from ARC into Phantom as events  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'add watchlist entry'
Add an entry to ARC Watchlist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_name** |  required  | Watchlist Name | string |  `digitalguardianarc watchlist name` 
**watchlist\_entry** |  required  | Entry value to be added to ARC Watchlist | string |  `digitalguardianarc watchlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.watchlist\_name | string |  `digitalguardianarc watchlist name` 
action\_result\.parameter\.watchlist\_entry | string |  `digitalguardianarc watchlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove watchlist entry'
Remove an entry from ARC Watchlist

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_name** |  required  | Watchlist Name | string |  `digitalguardianarc watchlist name` 
**watchlist\_entry** |  required  | Entry value to be removed from ARC Watchlist | string |  `digitalguardianarc watchlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.watchlist\_name | string |  `digitalguardianarc watchlist name` 
action\_result\.parameter\.watchlist\_entry | string |  `digitalguardianarc watchlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'check watchlist entry'
Check for an entry in ARC Watchlist

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_name** |  required  | Watchlist Name | string |  `digitalguardianarc watchlist name` 
**watchlist\_entry** |  required  | Entry value to be checked in ARC Watchlist | string |  `digitalguardianarc watchlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.watchlist\_name | string |  `digitalguardianarc watchlist name` 
action\_result\.parameter\.watchlist\_entry | string |  `digitalguardianarc watchlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add componentlist entry'
Add an entry to Componentlist

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist\_name** |  required  | Componentlist Name | string |  `digitalguardianarc componentlist name` 
**componentlist\_entry** |  required  | Entry value to be added to Componentlist | string |  `digitalguardianarc componentlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.componentlist\_name | string |  `digitalguardianarc componentlist name` 
action\_result\.parameter\.componentlist\_entry | string |  `digitalguardianarc componentlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove componentlist entry'
Remove an entry from Componentlist

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist\_name** |  required  | Componentlist Name | string |  `digitalguardianarc componentlist name` 
**componentlist\_entry** |  required  | Entry value to be removed from Componentlist | string |  `digitalguardianarc componentlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.componentlist\_name | string |  `digitalguardianarc componentlist name` 
action\_result\.parameter\.componentlist\_entry | string |  `digitalguardianarc componentlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'check componentlist entry'
Check for an entry in Componentlist

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**componentlist\_name** |  required  | Componentlist Name | string |  `digitalguardianarc componentlist name` 
**componentlist\_entry** |  required  | Entry value to be checked in Componentlist | string |  `digitalguardianarc componentlist entry` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.componentlist\_name | string |  `digitalguardianarc componentlist name` 
action\_result\.parameter\.componentlist\_entry | string |  `digitalguardianarc componentlist entry` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'on poll'
Ingest alerts from ARC into Phantom as events

Type: **ingest**  
Read only: **True**

The default start\_time is the past 5 days and the default end\_time is now\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start\_time** |  optional  | Start of time range, in epoch time \(milliseconds\) | numeric | 
**end\_time** |  optional  | End of time range, in epoch time \(milliseconds\) | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  optional  | Maximum number of artifact records to query for | numeric | 

#### Action Output
No Output