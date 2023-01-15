import json
import aiohttp
import asyncio
import aiofiles
import rich_click as click
import yaml
from pathlib import Path
from rich import print_json
from rich.console import Console
from jinja2 import Environment, FileSystemLoader
from gtts import gTTS

class NetboxGiftwrap():
    def __init__(self,
                url,
                token
            ):
        self.url = url
        self.token = token

    def netbox_giftwrap(self):
        asyncio.run(self.main())

    def netbox_api_list(self):
        self.api_list = [
            "/api/ipam/aggregates/",
            "/api/ipam/asns/",
            "/api/dcim/cables/",
            "/api/circuits/circuit-terminations/",
            "/api/circuits/circuit-types/",
            "/api/circuits/circuits/",
            "/api/virtualization/cluster-groups/",
            "/api/virtualization/cluster-types/",
            "/api/virtualization/clusters/",
            "/api/dcim/console-port-templates/",
            "/api/dcim/console-ports/",
            "/api/tenancy/contact-assignments/",
            "/api/tenancy/contact-groups/",
            "/api/tenancy/contact-roles/",
            "/api/tenancy/contacts/",
            "/api/dcim/device-bay-templates/",
            "/api/dcim/device-bays/",
            "/api/dcim/device-roles/",
            "/api/dcim/device-types/",
            "/api/dcim/devices/",
            "/api/dcim/front-port-templates/",
            "/api/dcim/front-ports/",
            "/api/users/groups/",
            "/api/dcim/interface-templates/",
            "/api/dcim/interfaces/",
            "/api/dcim/inventory-items/",
            "/api/ipam/ip-addresses/",
            "/api/ipam/ip-ranges/",
            "/api/dcim/locations/",
            "/api/dcim/manufacturers/",
            "/api/dcim/module-bay-templates/",
            "/api/dcim/module-bays/",
            "/api/dcim/module-types/",
            "/api/dcim/modules/",
            "/api/dcim/platforms/",
            "/api/dcim/power-feeds/",
            "/api/dcim/power-outlet-templates/",
            "/api/dcim/power-outlets/",
            "/api/dcim/power-panels/",
            "/api/dcim/power-port-templates/",
            "/api/dcim/power-ports/",
            "/api/ipam/prefixes/",
            "/api/circuits/provider-networks/",
            "/api/circuits/providers/",
            "/api/dcim/rack-reservations/",
            "/api/dcim/rack-roles/",
            "/api/dcim/racks/",
            "/api/dcim/rear-port-templates/",
            "/api/dcim/rear-ports/",
            "/api/dcim/regions/",
            "/api/ipam/rirs/",
            "/api/ipam/roles/",
            "/api/ipam/route-targets/",
            "/api/ipam/service-templates/",
            "/api/ipam/services/",
            "/api/dcim/site-groups/",
            "/api/dcim/sites/",
            "/api/status/",
            "/api/tenancy/tenant-groups/",
            "/api/tenancy/tenants/",
            "/api/users/tokens/",
            "/api/users/users/",
            "/api/dcim/virtual-chassis/",
            "/api/virtualization/interfaces/",
            "/api/virtualization/virtual-machines/",
            "/api/ipam/vlan-groups/",
            "/api/ipam/vlans/",
            "/api/ipam/vrfs/"
        ]
        return self.api_list        

    async def get_api(self,api_url):
        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Token { self.token }',
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}{api_url}", headers=headers, data=payload, verify_ssl=False) as resp:
                self.api_count += 1
                responseJSON = await resp.json()
                if api_url == "/api/status/":
                    responseList = responseJSON            
                else:
                    responseList = responseJSON['results']
                    offset = 50
                    total_pages = responseJSON['count'] / 50
                    while total_pages > 1:
                        async with session.get(f"{self.url}{api_url}?limit=50&offset={offset}", headers=headers, data=payload, verify_ssl=False) as resp:
                            self.api_count += 1
                            responseDict = await resp.json()
                            responseList.extend(responseDict['results'])
                            offset = offset +50
                            total_pages = total_pages - 1
                            print(f"{total_pages} pages remaining")
        return(api_url, responseList)

    async def main(self):
        self.api_count = 0
        self.file_count = 0
        api_list = self.netbox_api_list()
        results = await asyncio.gather(*(self.get_api(api_url) for api_url in api_list))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))
        click.secho(f"Netbox Giftwrap gathered data from { self.api_count } Netbox APIs",fg='green')
        click.secho(f"Netbox Giftwrap created { self.file_count } business ready reports",fg='green')

    async def json_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            async with aiofiles.open(f'{api}.json'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(json.dumps(payload, indent=4, sort_keys=True))
            self.file_count += 1

    async def yaml_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            clean_yaml = yaml.dump(payload, default_flow_style=False)
            async with aiofiles.open(f'{api}.yaml'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(clean_yaml)
            self.file_count += 1

    async def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('html.j2')
        for api, payload in json.loads(parsed_json):        
            html_output = await html_template.render_async(api = api,
                                         data_to_template = payload)
            async with aiofiles.open(f'{api}.html'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(html_output)
            self.file_count += 1

    async def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        md_template = env.get_template('md.j2')
        for api, payload in json.loads(parsed_json):        
            md_output = await md_template.render_async(api = api,
                                         data_to_template = payload)
            async with aiofiles.open(f'{api}.md'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(md_output)
            self.file_count += 1

    async def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('csv.j2')
        for api, payload in json.loads(parsed_json):        
            csv_output = await csv_template.render_async(api = api,
                                         data_to_template = payload)
            async with aiofiles.open(f'{api}.csv'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(csv_output)
            self.file_count += 1

    async def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('mindmap.j2')
        for api, payload in json.loads(parsed_json):        
            mindmap_output = await mindmap_template.render_async(api = api,
                                         data_to_template = payload)
            async with aiofiles.open(f'{api} mindmap.md'.replace("api","").replace("/"," "), 'w') as f:
                await f.write(mindmap_output)
            self.file_count += 1

    # async def mp3_file(self, parsed_json):
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mp3_template = env.get_template(f'mp3.j2')
    #     for api,payload in json.loads(parsed_json):
    #         language = 'en-US'
    #         if api == "/api/status/":
    #             mp3_output = await mp3_template.render_async(api = api,
    #                 data_to_template=payload)
    #             mp3 = gTTS(text = mp3_output, lang=language)
    #             # Save MP3
    #             mp3.save(f'{api} MP3.mp3'.replace("api","").replace("/"," "))

    #             self.file_count += 1
    #         else:        
    #             for result in payload:
    #                 mp3_output = await mp3_template.render_async(api = api,
    #                         result=result
    #                         )
    #                 mp3 = gTTS(text = mp3_output, lang=language)
    #                 # Save MP3
    #                 mp3.save(f'{api} {result["id"]} MP3.mp3'.replace("api","").replace("/"," "))
    #                 self.file_count += 1

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json), self.yaml_file(parsed_json), self.csv_file(parsed_json), self.markdown_file(parsed_json), self.html_file(parsed_json), self.mindmap_file(parsed_json))
        # self.mp3_file(parsed_json))

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
def cli(url,token):
    invoke_class = NetboxGiftwrap(url,token)
    invoke_class.netbox_giftwrap()

if __name__ == "__main__":
    cli()
