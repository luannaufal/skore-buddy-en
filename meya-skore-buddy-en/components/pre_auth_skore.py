from skore_api import Skore
from meya import Component

class PreAuthSkore(Component):
    
    def start(self):
    
        email = self.db.bot.settings["skore_user"]
        password = self.db.bot.settings["skore_key"]
        print("email", email)
        print("password", password)
        
        skore = Skore(email = email, password = password)

        self.db.bot.set("skore_token", {"token": skore.token, "expiration": skore.tokenExpiration})

        return self.respond(message = None, action = "next")