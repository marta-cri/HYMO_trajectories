## River masks Semi-authomatic Multi-Temporal extraction from Landsat SR images usign Google Earth Engine

Modified code from the Arctic_rivermasks branch for the use with service accounts and the auomatic dowload from drive.
For the automatic download you need to activate also the Drive API.
To authenticate the credentials are specified in the second code cell of the notebook, read below for a better understanding of the authentication process.

### Authentication process
To authenticate both Earth Engine and Drive you need to specify the name of the service account (the mail associated with it) in the <service_account> variable, the name of the json file where the credentials are stored in the <credentials_file> variable and the path of the folder where the file is stored in the <credentials_folder>. The author used a file that is placed in the same directory as the other scripts, but is not tracked on git to keep the credentials safe. In this file there is a function called <get_credentials> that takes no input and returns the value of this three variables.