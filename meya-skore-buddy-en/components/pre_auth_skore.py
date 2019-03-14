from skore_api import Skore
from meya import Component

class PreAuthSkore(Component):
    
    def start(self):
        
        tokenInfo = self.db.bot.get("skore_token")
        
        # If token still valid, then use it to avoid re-login
        if not tokenInfo or not Skore.tokenValid(tokenInfo["expiration"]):
            email = self.db.bot.settings["skore_user"]
            password = self.db.bot.settings["skore_key"]
            print("email", email)
            print("password", password)
            
            skore = Skore(email = email, password = password)
    
            self.db.bot.set("skore_token", {"token": skore.token, "expiration": skore.tokenExpiration})

        return self.respond(message = None, action = "next")