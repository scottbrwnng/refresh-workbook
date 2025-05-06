import keyring
from pathlib import Path
import tableauserverclient as tsc

# IMPORTANT!!!
# See the original repo here! https://github.com/CodingOnWindowsOS/Tableau/tree/main/Tableau%20Server%20Client

def push_workbook():
    # Setup
    # Store token name, token value, and site ID in variables.
    token_name = 'TSM'
    token_value = keyring.get_password('Tableau Server Management', 'TSM')
    site_id = 'sqlshortreads'    
    # Create authentication object using the token and site ID details.
    tableau_auth = tsc.PersonalAccessTokenAuth(token_name=token_name, personal_access_token=token_value, site_id=site_id)
    # Create a tableau server client object using specified server URL.
    server = tsc.Server('https://10ax.online.tableau.com')
    # Disable certificate verification. The next line of code may be required due to certificate issues.
    # server.add_http_options({'verify': False})

    # Sign-in to server.
    with server.auth.sign_in(tableau_auth):
        # Ensure the most recent Tableau REST API version is used.
        server.use_highest_version()
        # Create a filter for the project for which the workbook will be published.
        # There are multiple "Workbooks" projects, so the one with a parent project
        # name of "Europe Sales" must be identified.
        parent_project = server.projects.filter(name='Europe Sales')
        projects = server.projects.filter(name='Workbooks')
        project = [project for project in projects if project.parent_id == parent_project[0].id]

        # Configure the new workbook.
        new_workbook = tsc.WorkbookItem(
            name='Europe Sales: Open pipeline',
            project_id=project[0].id
        )

        # Publish the new workbook to the Tableau Server or Tableau Cloud instance.
        try:
            server.workbooks.publish(
                workbook_item=new_workbook,
                file=Path('C:\\path\\to\\workbook\\stgn.twbx'),
                mode='Overwrite', #see additional params here: https://tableau.github.io/server-client-python/docs/api-ref#workbooks
                connection_credentials=None,
                as_job=False
            )
        except:
            print(f'Unable to publish {new_workbook.name}.')
        else:
            print(f'{new_workbook.name} successfully published.')
            



def xml_replace(wb: xml) -> None:

    from pathlib import Path # never used this before..... 

    # Path to your Tableau workbook (.twb)
    input_path = Path("your_workbook.twb")
    output_path = Path("your_workbook_stgn.twb")

    # Read workbook content
    xml = input_path.read_text(encoding="utf-8")

    # Replace schema references
    xml = xml.replace("[dbo].", "[stgn].")

    # Save modified workbook
    output_path.write_text(xml, encoding="utf-8")

    #now this workbook can be uploaded to server using above func

    print(f"Updated workbook saved to: {output_path}")
