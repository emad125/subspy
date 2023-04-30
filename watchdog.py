import configparser
import asyncio
import hashlib
import logging
import httpx
import subprocess
from pymongo import MongoClient


class WatchDog:
    
    def __init__(self, config_file_path: str = 'config.ini'):
        
        self.domains, self.interval, self.threads, self.db = self._read_config_file(config_file_path)
        self.logger = self._configure_logger()
    
    def _read_config_file(self, config_file_path: str) -> tuple:
        
        config = configparser.ConfigParser()
        config.read(config_file_path)
        domains = config['scopes']['domains'].split(',')
        
        time_interval = config['settings']['interval']
        # Convert time interval to seconds
        if time_interval.endswith('s'):
            interval = int(time_interval[:-1])
        elif time_interval.endswith('m'):
            interval = int(time_interval[:-1]) * 60
        elif time_interval.endswith('h'):
            interval = int(time_interval[:-1]) * 3600
        else:
            raise ValueError('Invalid time interval format')
        
        threads = config['settings']['threads']
        mongo_uri = config['mongodb']['mongo_uri']
        mongo_db = config['mongodb']['mongo_db']
        
        mongo_client = MongoClient(mongo_uri)
        db = mongo_client[mongo_db]
        
        return (domains, interval, threads, db)

    def _configure_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger
    
    
    def _save_response(self, domain, subdomain, response):
        body_hash = hashlib.sha256(response.text.encode('utf-8')).hexdigest()
        #print(f"[*] {subdomain} sha256 {body_hash}")
        response_data = {
            'code': response.status_code,
            'headers':response.headers,
            'body': body_hash,
            'length': len(response.text)
        }
        #print(f"[*] {subdomain} response_data {response_data}")
        insert_response = self.db[domain].insert_one(
            {subdomain: response_data}
        )
        #print(f"[*] {subdomain} insert {insert_response}")

    def _check_subdomain(self, domain: str, subdomain: str) -> None:
        urls = [f'https://{subdomain}', f'http://{subdomain}']
        for url in urls:
            try:
                response = httpx.get(url, verify = False)
                #print(f"[*] {url} {response.status_code}")
                self._save_response(domain, subdomain, response)

            except httpx.ConnectTimeout as e:
                print(f"[ConnectTimeout] on checking subdomain {url}: {e}")
                pass
            except httpx.ConnectError as e:
                print(f"[ConnectError] on checking subdomain {url}: {e}")
                pass
            except httpx.ReadTimeout as e:
                print(f"[ReadTimeout] on checking subdomain {url}: {e}")
                pass
            except httpx.RemoteProtocolError as e:
                print(f"[RemoteProtocolError] on checking subdomain {url}: {e}")
                pass
                
            
    async def _enumerate_subdomains(self, domain):
        #try:
        cmd = ['subfinder', '-d', domain, '-all', '-silent']
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
        subdomains = [domain for domain in output.decode().split('\n') if domain != '']
        #print(f"[*] Found {len(subdomains)} subdomains for {domain}")
        for subdomain in subdomains:
            self._check_subdomain(domain, subdomain)
        #except Exception as e:
        #    print(f"Error enumerating subdomains for {domain}: {e}")

    async def run(self):
        for domain in self.domains:
            #print(f"[*] Enumerating {domain}")
            await self._enumerate_subdomains(domain)

    def close(self):
        self.client.close()


async def main():
    watchdog = WatchDog('config.ini')
    await watchdog.run()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

