import sys
import os
import json
import requests
import rich_click as click
import yaml
from pathlib import Path
from rich import print_json
from rich.console import Console
from jinja2 import Environment, FileSystemLoader
from gtts import gTTS

class GetJson():
    def __init__(self,
                url,
                token,
                api,
                filetype,
            ):
        self.url = url
        self.token = token
        self.api = api
        self.filetype = filetype
        self.supported_apis = ['aggregates',
                               'asns',
                               'cables',
                               'circuit-terminations',
                               'circuit-types',
                               'circuits',
                               'cluster-groups',
                               'cluster-types',
                               'clusters',
                               'console-port-templates',
                               'console-ports',
                               'contact-assignments',
                               'contact-groups',
                               'contact-roles',
                               'contacts',
                               'device-bay-templates',
                               'device-bays',
                               'device-roles',
                               'device-types',
                               'devices',
                               'front-port-templates',
                               'front-ports',
                               'groups',
                               'interface-templates',
                               'interfaces',
                               'inventory-items',
                               'ip-addresses',
                               'ip-ranges',
                               'locations',
                               'manufacturers',
                               'module-bay-templates',
                               'module-bays',
                               'module-types',
                               'modules',
                               'platforms',
                               'power-feeds',
                               'power-outlet-templates',
                               'power-outlets',
                               'power-panels',
                               'power-port-templates',
                               'power-ports',
                               'prefixes',
                               'provider-networks',
                               'providers',
                               'rack-reservations',
                               'rack-roles',
                               'racks',
                               'rear-port-templates',
                               'rear-ports',
                               'regions',
                               'rirs',
                               'roles',
                               'route-targets',
                               'service-templates',
                               'services',
                               'site-groups',
                               'sites',
                               'status',
                               'tenant-groups',
                               'tenants',
                               'tokens',
                               'users',
                               'virtual-chassis',
                               'virtual-interfaces',
                               'virtual-machines',
                               'vlan-groups',
                               'vlans',
                               'vrfs'
                               ]

    def netbox_giftwrap(self):
        if self.api == "all":
            for single_api in self.supported_apis:
                self.api = single_api
                parsed_json = json.dumps(self.capture_state(), indent=4, sort_keys=True)
                if self.filetype != "none":
                    self.pick_filetype(parsed_json)
                else:
                    print_json(parsed_json)                
        if self.api == "?":
            for single_api in self.supported_apis:
                click.secho(f"{single_api}", fg='green')
        parsed_json = json.dumps(self.capture_state(), indent=4, sort_keys=True)
        if self.filetype != "none":
            self.pick_filetype(parsed_json)
        else:
            print_json(parsed_json)

    def capture_state(self):
        if self.api == "aggregates":
            url = f"{ self.url }/api/ipam/aggregates/"
        elif self.api == "asns":
            url = f"{ self.url }/api/ipam/asns/"
        elif self.api == "cables":
            url = f"{ self.url }/api/dcim/cables/"            
        elif self.api == "circuit-terminations":
            url = f"{ self.url }/api/circuits/circuit-terminations/"
        elif self.api == "circuit-types":
            url = f"{ self.url }/api/circuits/circuit-types/"
        elif self.api == "circuits":
            url = f"{ self.url }/api/circuits/circuits"
        elif self.api == "cluster-groups":
            url = f"{ self.url }/api/virtualization/cluster-groups/"
        elif self.api == "cluster-types":
            url = f"{ self.url }/api/virtualization/cluster-types/"
        elif self.api == "clusters":
            url = f"{ self.url }/api/virtualization/clusters/"
        elif self.api == "console-port-templates":
            url = f"{ self.url }/api/dcim/console-port-templates/"
        elif self.api == "console-ports":
            url = f"{ self.url }/api/dcim/console-ports/"
        elif self.api == "contact-assignments":
            url = f"{ self.url }/api/tenancy/contact-assignments/"
        elif self.api == "contact-groups":
            url = f"{ self.url }/api/tenancy/contact-groups/"
        elif self.api == "contact-roles":
            url = f"{ self.url }/api/tenancy/contact-roles/"
        elif self.api == "contacts":
            url = f"{ self.url }/api/tenancy/contacts/"            
        elif self.api == "device-bay-templates":
            url = f"{ self.url }/api/dcim/device-bay-templates/"
        elif self.api == "device-bays":
            url = f"{ self.url }/api/dcim/device-bays/"
        elif self.api == "device-roles":
            url = f"{ self.url }/api/dcim/device-roles/"
        elif self.api == "device-types":
            url = f"{ self.url }/api/dcim/device-types/"
        elif self.api == "devices":
            url = f"{ self.url }/api/dcim/devices/"
        elif self.api == "front-port-templates":
            url = f"{ self.url }/api/dcim/front-port-templates/"
        elif self.api == "front-ports":
            url = f"{ self.url }/api/dcim/front-ports/"
        elif self.api == "groups":
            url = f"{ self.url}/api/users/groups/"
        elif self.api == "interface-templates":
            url = f"{ self.url }/api/dcim/interface-templates/"
        elif self.api == "interfaces":
            url = f"{ self.url }/api/dcim/interfaces/"
        elif self.api == "inventory-items":
            url = f"{ self.url }/api/dcim/inventory-items/"
        elif self.api == "ip-addresses":
            url = f"{ self.url }/api/ipam/ip-addresses/"
        elif self.api == "ip-ranges":
            url = f"{ self.url }/api/ipam/ip-ranges/"
        elif self.api == "locations":
            url = f"{ self.url }/api/dcim/locations/"            
        elif self.api == "manufacturers":
            url = f"{ self.url }/api/dcim/manufacturers/"
        elif self.api == "module-bay-templates":
            url = f"{ self.url }/api/dcim/module-bay-templates/"
        elif self.api == "module-bays":
            url = f"{ self.url }/api/dcim/module-bays/"
        elif self.api == "module-types":
            url = f"{ self.url }/api/dcim/module-types/"
        elif self.api == "modules":
            url = f"{ self.url }/api/dcim/modules/"
        elif self.api == "platforms":
            url = f"{ self.url }/api/dcim/platforms/"
        elif self.api == "power-feeds":
            url = f"{ self.url }/api/dcim/power-feeds/"
        elif self.api == "power-outlet-templates":
            url = f"{ self.url }/api/dcim/power-outlet-templates/"
        elif self.api == "power-outlets":
            url = f"{ self.url }/api/dcim/power-outlets/"
        elif self.api == "power-panels":
            url = f"{ self.url }/api/dcim/power-panels/"
        elif self.api == "power-port-templates":
            url = f"{ self.url }/api/dcim/power-port-templates/"
        elif self.api == "power-ports":
            url = f"{ self.url }/api/dcim/power-ports/"
        elif self.api == "prefixes":
            url = f"{ self.url }/api/ipam/prefixes/"
        elif self.api == "provider-networks":
            url = f"{ self.url }/api/circuits/provider-networks/"
        elif self.api == "providers":
            url = f"{ self.url }/api/circuits/providers/"
        elif self.api == "rack-reservations":
            url = f"{ self.url }/api/dcim/rack-reservations/"
        elif self.api == "rack-roles":
            url = f"{ self.url }/api/dcim/rack-roles/"
        elif self.api == "racks":
            url = f"{ self.url }/api/dcim/racks/"
        elif self.api == "rear-port-templates":
            url = f"{ self.url }/api/dcim/rear-port-templates/"
        elif self.api == "rear-ports":
            url = f"{ self.url }/api/dcim/rear-ports/"
        elif self.api == "regions":
            url = f"{ self.url }/api/dcim/regions/"
        elif self.api == "rirs":
            url = f"{ self.url }/api/ipam/rirs/"
        elif self.api == "roles":
            url = f"{ self.url }/api/ipam/roles/"
        elif self.api == "route-targets":
            url = f"{ self.url }/api/ipam/route-targets/"
        elif self.api == "service-templates":
            url = f"{ self.url }/api/ipam/service-templates/"
        elif self.api == "services":
            url = f"{ self.url }/api/ipam/services/"
        elif self.api == "site-groups":
            url = f"{ self.url }/api/dcim/site-groups/"
        elif self.api == "sites":
            url = f"{ self.url }/api/dcim/sites/"
        elif self.api == "status":
            url = f"{ self.url }/api/status/"            
        elif self.api == "tenant-groups":
            url = f"{ self.url }/api/tenancy/tenant-groups/"
        elif self.api == "tenants":
            url = f"{ self.url }/api/tenancy/tenants/"
        elif self.api == "tokens":
            url = f"{ self.url }/api/users/tokens/"
        elif self.api == "users":
            url = f"{ self.url }/api/users/users/"            
        elif self.api == "virtual-chassis":
            url = f"{ self.url }/api/dcim/virtual-chassis/"
        elif self.api == "virtual-interfaces":
            url = f"{ self.url }/api/virtualization/interfaces/"
        elif self.api == "virtual-machines":
            url = f"{ self.url }/api/virtualization/virtual-machines/"            
        elif self.api == "vlan-groups":
            url = f"{ self.url }/api/ipam/vlan-groups/"
        elif self.api == "vlans":
            url = f"{ self.url }/api/ipam/vlans/"
        elif self.api == "vrfs":
            url = f"{ self.url }/api/ipam/vrfs/"
        else:
            click.secho(f"{ self.api } is not a supported API. Please check the README for a list of supported APIs", fg='red')
            sys.exit()
        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Token { self.token }',
            }
        if self.api == "status":
            response = requests.request("GET", url, headers=headers, data=payload)
            responseJSON = response.json()
            responseList = responseJSON            
        else:
            response = requests.request("GET", url, headers=headers, data=payload)
            responseJSON = response.json()
            responseList = responseJSON['results']
            offset = 50
            total_pages = responseJSON['count'] / 50
            while total_pages > 1:
                response = requests.request("GET", f"{url}?limit=50&offset={offset}", headers=headers, data=payload)
                responseList.extend(response.json()['results'])
                offset = offset +50
                total_pages = total_pages - 1
                print(f"{total_pages} pages remaining")
        return(responseList)

    def pick_filetype(self, parsed_json):
        if self.filetype == "none":
            pass
        elif self.filetype == 'json':
            self.json_file(parsed_json)
        elif self.filetype == 'yaml':
            self.yaml_file(parsed_json)
        elif self.filetype == 'csv':
            self.csv_file(parsed_json)
        elif self.filetype == 'html':
            self.html_file(parsed_json)
        elif self.filetype == 'markdown':
            self.markdown_file(parsed_json)
        elif self.filetype == 'mindmap':
            self.mindmap_file(parsed_json)
        elif self.filetype == 'mp3':
            self.mp3_file(parsed_json)
        elif self.filetype == 'all':
            self.all_files(parsed_json)

    def json_file(self, parsed_json):
        with open(f'{self.api}.json', 'w') as f:
            f.write(parsed_json)
        click.secho(f"JSON file created at { sys.path[0] }/{self.api}.json",
        fg='green')

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        with open(f'{self.api}.yaml', 'w') as f:
            f.write(clean_yaml)
        click.secho(f"YAML file created at { sys.path[0] }/{self.api}.yaml",
        fg='green')

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template(f'html.j2')
        html_output = html_template.render(api = self.api,
                data_to_template=json.loads(parsed_json))
        with open(f'{self.api}.html', 'w') as f:
            f.write(html_output)
        click.secho(f"HTML file created at { sys.path[0] }/{self.api}.html",
            fg='green')

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template(f'md.j2')
        markdown_output = markdown_template.render(api = self.api,
                    data_to_template=json.loads(parsed_json))
        with open(f'{self.api}.md', 'w') as f:
            f.write(markdown_output)
        click.secho(f"Markdown file created at { sys.path[0] }/{self.api}.md",
            fg='green')

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('csv.j2')
        csv_output = csv_template.render(api = self.api,
            data_to_template=json.loads(parsed_json))
        with open(f'{self.api}.csv', 'w') as f:
            f.write(csv_output)
        click.secho(f"CSV file created at { sys.path[0] }/{self.api}.csv",
            fg='green')

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template(f'mindmap.j2')
        json_results = json.loads(parsed_json)
        if self.api == "status":
            mindmap_output = mindmap_template.render(api = self.api,
                data_to_template=json_results)
            with open(f'{self.api} mindmap.md', 'w') as f:
                f.write(mindmap_output)
            click.secho(f'Mindmap file created at { sys.path[0] }/{self.api} mindmap.md',
                fg='green')
        else:
            for result in json_results:
                mindmap_output = mindmap_template.render(api = self.api,
                        result=result
                        )
                with open(f'{self.api} {result["id"]} mindmap.md', 'w') as f:
                    f.write(mindmap_output)
                click.secho(f'Mindmap file created at { sys.path[0] }/{self.api} {result["id"]} mindmap.md',
                    fg='green')

    def mp3_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mp3_template = env.get_template(f'mp3.j2')
        json_results = json.loads(parsed_json)
        language = 'en-US'
        if self.api == "status":
            mp3_output = mp3_template.render(api = self.api,
                data_to_template=json_results)
            mp3 = gTTS(text = mp3_output, lang=language)
            # Save MP3
            mp3.save(f'{self.api} MP3.mp3')

            click.secho(f'MP3 file created at { sys.path[0] }/{self.api} mindmap.md',
                fg='green')
        else:        
            for result in json_results:
                mp3_output = mp3_template.render(api = self.api,
                        result=result
                        )
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'{self.api} {result["id"]} MP3.mp3')
                click.secho(
                    f"MP3 file created at { sys.path[0] }/{self.api} {result['id']} MP3.mp3",
                    fg='green')

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.html_file(parsed_json)
        self.markdown_file(parsed_json)
        self.csv_file(parsed_json)
        self.mindmap_file(parsed_json)
        self.mp3_file(parsed_json)

@click.command()
@click.option('--url',
    prompt='NetBox URL',
    help='NextBox URL',
    required=True, envvar="URL")
@click.option('--token',
    prompt='NetBox API Token',
    help='NetBox API Token',
    hide_input=True,
    required=True,
    envvar="TOKEN")
@click.option('--api',
    prompt='NetBox API',
    help='NetBox API',
    required=True)
@click.option('--filetype',
    prompt='Filetype',
    type=click.Choice(['none',
                        'json',
                        'yaml',
                        'html',
                        'csv',
                        'markdown',
                        'mindmap',
                        'mp3',
                        'all'],
        case_sensitive=True),
    help='Filetype to output API to',
    required=False,
    default='none')
def cli(url,
        token,
        api,
        filetype,
        ):
    invoke_class = GetJson(url,
                            token,
                            api,
                            filetype,
                        )
    invoke_class.netbox_giftwrap()

if __name__ == "__main__":
    cli()
