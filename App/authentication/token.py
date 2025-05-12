import logging
import requests
import configparser
from datetime import datetime, timedelta, timezone
from typing import Optional
from dataclasses import dataclass, field
import os

@dataclass
class AuthService:
    logger: logging.Logger = field(init=True)
    url: str
    credential: str
    token: Optional[str] = field(default=None, init=False)
    expiration: Optional[datetime] = field(default=None, init=False)
    key_file: str = "token.ini" 
    

    def load_token_from_file(self) -> bool:
        """Carga el token y la expiración desde el archivo key.init si existe."""
        config = configparser.ConfigParser()
        
        if os.path.exists(self.key_file):
            try:
                config.read(self.key_file)
                if 'PASSWORD' in config:
                    saved_token = config['PASSWORD'].get('TOKEN')
                    expiration_str = config['PASSWORD'].get('EXPIRATION')
                    if saved_token and expiration_str:
                        self.token = saved_token
                        self.expiration = datetime.fromisoformat(expiration_str)
                        return True
            except Exception as e:
                self.logger.error(f"Failed while reading the file {self.key_file}: {e}")
        return False

    def save_token_to_file(self) -> None:
        """Guarda el token y la fecha de expiración en el archivo key.init."""
        if self.token and self.expiration:
            config = configparser.ConfigParser()
            try:
                if not config.has_section('PASSWORD'):
                    config.add_section('PASSWORD')

                config['PASSWORD'] = {
                    'TOKEN': self.token,
                    'EXPIRATION': self.expiration.isoformat()
                }
                with open(self.key_file, 'w') as file:
                    config.write(file)
            except Exception as e:
                self.logger.error(f"Error at saving the file {self.key_file}: {e}")

    def get_token(self, autherization:bool=True) -> str:
        """Obtiene el token, primero verificando si existe uno válido en el archivo."""
        self.logger.info("REACIONAAAA")
        if self.load_token_from_file() and self.is_token_valid() and autherization:
            self.logger.info("Token exitente y validado")
            return self.token  

        self.logger.info("Token is nor valid. Getting the token...")
        
        payload = {"credential": self.credential}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()  

            data = response.json()
            self.token = data.get("token")
            expiration_str = data.get("expiration")

            if self.token and expiration_str:
                try:
                    self.expiration = datetime.fromisoformat(expiration_str)
                    self.save_token_to_file()  
                    return self.token
                
                except ValueError:
                    self.logger.error("Date format is invalid.")
            else:
                self.logger.info("No token or expiration date found.")
        except requests.RequestException as e:
            self.logger.error(f"Error sending the request: {e}")

        return ""  

    def is_token_valid(self) -> bool:
        """Verifica si el token es válido y no ha expirado."""
        if self.token and self.expiration:
            now = datetime.now(timezone.utc)
            if self.expiration <= now or self.expiration - now < timedelta(days=60):
                return False
            return True
        return False

 